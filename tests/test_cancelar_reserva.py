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
    Estacionamiento)


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
    
def crear_factura(_reserva, monto):
    pago = Pago(
            reserva = _reserva,
            id = asigna_id_unico(),
            fechaTransaccion = datetime.now(),
            cedula = "10",
            cedulaTipo = "V",
            tarjetaTipo = "Vista",
            monto = Decimal(monto)
    )
    pago.save()
    
def crear_pago(h_inicio, h_fin, monto):
    p = crear_propietario()
    e = crear_estacionamiento(p)
    r = crear_reserva(h_inicio, h_fin, e)
    crear_factura(r, monto)

def cancelar_reservacion(id_pago, id_billetera, tiempo = datetime.now() + timedelta(seconds = 60), monto_debitar = 0):
    try:
        pago = Pago.objects.get(pk = id_pago)
        billetera = BilleteraElectronica.objects.get(pk = id_billetera)
        if ((pago.validar_cancelacion(tiempo)) and 
            (billetera.validar_recarga(pago.monto))):
            c = Cancelaciones(
                  pagoCancelado = pago,
                  billetera = billetera,
                  id = asigna_id_unico(),
                  monto = pago.monto,
                  fechaTransaccion = datetime.now()            
            )
            pago.cancelar_reserva()
            billetera.recargar_saldo(pago.monto)
            c.save()
    except:
        pass
        
    
       
        
class TestCancelarReserva(TestCase):
    
    # borde
    def testCancelarUnaReservacion(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, monto)
        crear_billetera()
        cancelar_reservacion(1, 1)
        p = Pago.objects.get(pk = 1)
        b = BilleteraElectronica.objects.get(pk = 1)
        self.assertTrue(p.cancelado and b.saldo == monto)
    
    # borde    
    def testCancelarReservacionMontoCero(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = 0
        crear_pago(inicio, fin, monto)
        crear_billetera()
        cancelar_reservacion(1, 1)
        self.assertEqual(len(Cancelaciones.objects.all()), 0)
        
    # borde
    def testCancelarReservacionMontoMaximo(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = 10000
        crear_pago(inicio, fin, monto)
        crear_billetera()
        cancelar_reservacion(1, 1)
        p = Pago.objects.get(pk = 1)
        b = BilleteraElectronica.objects.get(pk = 1)
        self.assertTrue(p.cancelado and b.saldo == monto)
        
    # borde
    def testCancelarReservacionBilleteraFull(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, monto)
        crear_billetera(10000)
        cancelar_reservacion(1, 1)
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 0)
      
    # malicia
    def testCancelarDosVeces(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = 50
        crear_pago(inicio, fin, monto)
        crear_billetera()
        cancelar_reservacion(1, 1)
        cancelar_reservacion(1, 1)
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 1)
        
    # malicia
    def TestCancelarReservaNoExiste(self):
        crear_billetera()
        cancelar_reservacion(1, 1)
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 0)
    
       
    # malicia
    def TestCancelarReservaBilleteraNoExiste(self):
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, monto)
        cancelar_reservacion(1, 1)
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 0)
        
    # borde
    def TestCancelarReservaAntes(self):
        inicio = datetime(2015, 6, 4, 8, 5, 0, 0)
        fin = datetime(2015, 6, 4, 9, 5, 0, 0)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, monto)
        crear_billetera(10000)
        cancelar_reservacion(1, 1, datetime(2015, 6, 4, 8, 4, 0, 0))
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 1)
        
    # borde
    def TestCancelarReservaDurante(self):
        inicio = datetime(2015, 6, 4, 8, 5, 0, 0)
        fin = datetime(2015, 6, 4, 9, 5, 0, 0)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, monto)
        crear_billetera(10000)
        cancelar_reservacion(1, 1, datetime(2015, 6, 4, 8, 5, 0, 0))
        cancelaciones = Cancelaciones.objects.all()
        self.assertEqual(len(cancelaciones), 0)