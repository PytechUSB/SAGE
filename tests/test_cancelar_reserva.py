# -*- coding: utf-8 -*-

from django.test import TestCase

from decimal import Decimal
from datetime import (
    datetime,
    timedelta,
)
from estacionamientos.controller import (
    pago_autenticar, 
    billetera_autenticar
, asigna_id_unico)

from estacionamientos.models import (
    Reserva,
    Pago,
    BilleteraElectronica,
    Recargas,
    Cancelaciones,
    Propietario,
    Estacionamiento, AdministracionSage)


def crear_propietario():
    p = Propietario(
            nombres = "Daniel",
            apellidos = "Añes",
            cedula = "10"
    )
    p.save()
    return p
    
def crear_estacionamiento(_propietario):
    e = Estacionamiento(
            nombre = "Estacionamiento1",
            direccion = "Calle Aqui",
            rif = "J-123456789",
            propietario = _propietario           
    )
    e.save()
    return e
    
def crear_reserva(h_inicio, h_fin, _estacionamiento):
    r = Reserva(
            estacionamiento = _estacionamiento,
            inicioReserva = h_inicio,
            finalReserva = h_fin    
    )
    r.save()
    return r
    
def crear_billetera(monto = 0):
    r = BilleteraElectronica(
            nombre = "Daniel",
            apellido = "Nuñez",
            cedula = "10",
            cedulaTipo = "V",
            PIN = "1234",
            saldo = monto                 
    )
    r.save()
    
def crear_factura(_reserva, monto, tarjetaTipo, id_billetera):
    pago = Pago(
            reserva = _reserva,
            id = asigna_id_unico(),
            fechaTransaccion = datetime.now(),
            cedula = "10",
            cedulaTipo = "V",
            tarjetaTipo = tarjetaTipo,
            monto = Decimal(monto),
            idBilletera = id_billetera
    )
    pago.save()
    
def crear_pago(h_inicio, h_fin, monto, tarjetaTipo = 'Vista', id_billetera = None):
    p = crear_propietario()
    e = crear_estacionamiento(p)
    r = crear_reserva(h_inicio, h_fin, e)
    crear_factura(r, monto, tarjetaTipo, id_billetera)

def cancelar_reservacion(id_pago, id_billetera, monto_debitar, tiempo = datetime.now() + timedelta(seconds = 60)):
    try:
        pago = Pago.objects.get(pk = id_pago)
        billetera = BilleteraElectronica.objects.get(pk = id_billetera)
        if ((pago.validar_cancelacion(tiempo)) and 
            (billetera.validar_recarga(pago.monto - monto_debitar))):
            c = Cancelaciones(
                  pagoCancelado = pago,
                  billetera = billetera,
                  id = asigna_id_unico(),
                  monto = pago.monto,
                  fechaTransaccion = datetime.now()            
            )
            pago.cancelar_reserva()
            billetera.recargar_saldo(pago.monto - monto_debitar)
            c.save()

    except:
        pass
                
class TestCancelarReserva(TestCase):
    
    # borde
    def testCancelarUnaReservacion(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = Decimal('0.01')
        crear_billetera()
        crear_pago(inicio, fin, monto, 'Billetera Electronica', 1)
        cancelar_reservacion(1, 1, monto_debitar = 0)
        p = Pago.objects.get(pk = 1)
        b = BilleteraElectronica.objects.get(pk = 1)
        self.assertTrue(p.cancelado and b.saldo == monto)
    
    # borde    
    def testCancelarReservacionMontoCero(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = 0
        crear_pago(inicio, fin, monto, 'Billetera Electronica', 1)
        crear_billetera()
        cancelar_reservacion(1, 1, monto_debitar = 0)
        self.assertEqual(len(Cancelaciones.objects.all()), 0)
        
    # borde
    def testCancelarReservacionMontoMaximo(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = 10000
        crear_pago(inicio, fin, monto, 'Vista')
        crear_billetera()
        admin = AdministracionSage.objects.get(pk = 1)
        p = Pago.objects.get(pk = 1)
        aplicaCargo = p.factura_inicial_pagada_billetera()
        if aplicaCargo:
            monto_debitar = admin.calcular_monto(monto)
            
        else:
            monto_debitar = 0
        cancelar_reservacion(1, 1, monto_debitar)
        p = Pago.objects.get(pk = 1)
        b = BilleteraElectronica.objects.get(pk = 1)
        self.assertTrue(p. cancelado and b.saldo == 9010)
        
    # borde
    def testCancelarReservacionBilleteraFull(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, monto)
        crear_billetera(10000)
        cancelar_reservacion(1, 1, monto_debitar = 0)
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 0)
      
    # malicia
    def testCancelarDosVeces(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = 50
        crear_pago(inicio, fin, monto)
        crear_billetera()
        cancelar_reservacion(1, 1, monto_debitar = 0)
        cancelar_reservacion(1, 1, monto_debitar = 0)
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 1)
        
    # malicia
    def TestCancelarReservaNoExiste(self):
        crear_billetera()
        cancelar_reservacion(1, 1, 0)
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 0)
    
       
    # malicia
    def TestCancelarReservaBilleteraNoExiste(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, monto)
        cancelar_reservacion(1, 1, 0)
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 0)
        
    # borde
    def TestCancelarReservaAntes(self):
        inicio = datetime(2015, 6, 4, 8, 5, 0, 0)
        fin = datetime(2015, 6, 4, 9, 5, 0, 0)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, monto)
        crear_billetera(10000)
        cancelar_reservacion(1, 1, 0, datetime(2015, 6, 4, 8, 4, 0, 0))
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 1)
        
    # borde
    def TestCancelarReservaDurante(self):
        inicio = datetime(2015, 6, 4, 8, 5, 0, 0)
        fin = datetime(2015, 6, 4, 9, 5, 0, 0)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, monto)
        crear_billetera(10000)
        cancelar_reservacion(1, 1, 0, datetime(2015, 6, 4, 8, 5, 0, 0))
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 0)
    
    # interno
    def testCancelarReservaPagadaBilletera(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = 100
        crear_billetera()
        crear_pago(inicio, fin, monto, 'Billetera Electronica', 1)
        admin = AdministracionSage.objects.get(pk = 1)
        p = Pago.objects.get(pk = 1)
        aplicaCargo = p.factura_inicial_pagada_billetera()
        if aplicaCargo:
            monto_debitar = admin.calcular_monto(monto)
            
        else:
            monto_debitar = 0
        cancelar_reservacion(1, 1, monto_debitar)
        p = Pago.objects.get(pk = 1)
        b = BilleteraElectronica.objects.get(pk = 1)
        self.assertTrue(p. cancelado and b.saldo == 100)
        
    # interno
    def testCancelarReservaPagadaTarjetaCredito(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = 100
        crear_billetera()
        crear_pago(inicio, fin, monto, 'Vista', 1)
        admin = AdministracionSage.objects.get(pk = 1)
        p = Pago.objects.get(pk = 1)
        aplicaCargo = p.factura_inicial_pagada_billetera()
        if aplicaCargo:
            monto_debitar = admin.calcular_monto(monto)
            
        else:
            monto_debitar = 0
        cancelar_reservacion(1, 1, monto_debitar)
        p = Pago.objects.get(pk = 1)
        b = BilleteraElectronica.objects.get(pk = 1)
        self.assertTrue(p. cancelado and b.saldo == Decimal('90.1'))