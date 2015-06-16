# -*- coding: utf-8 -*-

from django.test import TestCase

from decimal import Decimal

from datetime import timedelta, time

from estacionamientos.models import (
    Pago, 
    Recargas,
    Cancelaciones,
    BilleteraElectronica, 
    Propietario, 
    Estacionamiento,
    Reserva,
    PagoOperacionesEspeciales,
    AdministracionSage
)
from estacionamientos.controller import (
    asigna_id_unico, 
    validarHorarioReserva, 
    validarHorarioReservaMover,
    marzullo
)

from datetime import datetime
def crear_propietario():
    p = Propietario(
            nombres = "Daniel",
            apellidos = "Añes",
            cedula = "10"
    )
    p.save()
    return p
    
def crear_estacionamiento(_propietario, horizonte):
    e = Estacionamiento(
            nombre = "Estacionamiento1",
            direccion = "Calle Aqui",
            rif = "J-123456789",
            propietario = _propietario,
            capacidad = 1,
            horizonte = horizonte,
            apertura = time(0, 0),
            cierre = time(23, 59)       
    )
    e.save()
    return e

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
    
def crear_reserva(h_inicio, h_fin, _estacionamiento):
    r = Reserva(
            estacionamiento = _estacionamiento,
            inicioReserva = h_inicio,
            finalReserva = h_fin    
    )
    r.save()
    return r
    
def crear_factura(_reserva, monto, tarjetaTipo):
    pago = Pago(
            reserva = _reserva,
            id = asigna_id_unico(),
            fechaTransaccion = datetime.now(),
            cedula = "10",
            cedulaTipo = "V",
            tarjetaTipo = tarjetaTipo,
            monto = Decimal(monto)
    )
    pago.save()
    
def crear_pago(h_inicio, h_fin, monto, estacionamiento, tarjetaTipo):
    r = crear_reserva(h_inicio, h_fin, estacionamiento)
    crear_factura(r, monto, tarjetaTipo)
    
def pago_mover_reserva(idPagoAMover, h_inicio, h_fin, diferencia, estacionamiento, tarjetaTipo):
    pagoAnterior = Pago.objects.get(pk = idPagoAMover)
    crear_pago(h_inicio, h_fin, pagoAnterior.monto + diferencia, estacionamiento, tarjetaTipo)
    cancelacion = Cancelaciones(
        id = asigna_id_unico(),
        pagoCancelado = pagoAnterior,
        monto = 0,
        fechaTransaccion = datetime.now()    
    )
    cancelacion.save()
    pagoAnterior.fue_movido()
    
    validarHorarioReserva,
def recarga_mover_reserva(idPagoAMover, h_inicio, h_fin, diferencia, id_billetera, estacionamiento, tarjetaTipo):
    pagoAnterior = Pago.objects.get(pk = idPagoAMover)
    billetera = BilleteraElectronica.objects.get(pk = id_billetera)
    montoARecargar = diferencia
    crear_pago(h_inicio, h_fin, pagoAnterior.monto - montoARecargar, estacionamiento, tarjetaTipo)
    cancelacion = Cancelaciones(
        id = asigna_id_unico(),
        pagoCancelado = pagoAnterior,
        billetera = billetera,
        monto = montoARecargar,
        fechaTransaccion = datetime.now()    
    )
    cancelacion.save()
    pagoAnterior.fue_movido()
    billetera.recargar_saldo(montoARecargar)

class MoverReservaTestCase(TestCase):
    
    # interno
    def testMoverReservaSolapada(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Billetera Electronica'
        p = crear_propietario()
        e = crear_estacionamiento(p, 168)
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        monto = Decimal('0.01')
        crear_pago(inicio, fin, Decimal('0.01'), e, tarjetaTipo)
        pago = Pago.objects.get(pk = 1)
        administracion = AdministracionSage.objects.get(pk = 1)
        if pago.tarjetaTipo != 'Billetera Electronica':
            monto_debitar = administracion.calcular_monto(monto)
        else:
            if pago.facturaMovida != None:
                monto_debitar = administracion.calcular_monto(monto)
            else:
                monto_debitar = 0
                
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, 168) and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, 0, e, tarjetaTipo)
        pagos = Pago.objects.filter(fueMovido = True)
        self.assertTrue(len(pagos) == 1 and monto_debitar == 0)
    
    
    # interno    
    def testMoverReservaMontoMayor(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Vista'
        p = crear_propietario()
        e = crear_estacionamiento(p, 168)
        monto = 10
        nuevo_monto = 100
        diferencia = Decimal(90)
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        crear_pago(inicio, fin, monto, e, tarjetaTipo)
        pago = Pago.objects.get(pk = 1)
        administracion = AdministracionSage.objects.get(pk = 1)
        if pago.tarjetaTipo != 'Billetera Electronica':
            monto_debitar = administracion.calcular_monto(monto)
        else:
            if pago.facturaMovida != None:
                monto_debitar = administracion.calcular_monto(monto)
            else:
                monto_debitar = 0

        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, 168) and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, diferencia, e, tarjetaTipo)
        pago = Pago.objects.get(pk = 2)
        self.assertEqual(pago.monto, monto + diferencia)
    '''
    # interior    
    def testMoverReservaMontoMenor(self):
        p = crear_propietario()
        e = crear_estacionamiento(p)
        monto = Decimal('0.01')
        diferencia = Decimal('5')
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        crear_pago(inicio, fin, monto, e)
        crear_billetera()
        recarga_mover_reserva(1, inicio, fin, diferencia, 1, e)
        billetera = BilleteraElectronica.objects.get(pk = 1)
        self.assertEqual(billetera.saldo, diferencia)
    
    # malicia  
    def testMoverReservaAlPasado(self):
        p = crear_propietario()
        e = crear_estacionamiento(p)
        monto = Decimal('0.01')
        diferencia = 0
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        crear_pago(inicio, fin, monto, e)
        crear_billetera()
        recarga_mover_reserva(1, datetime.now() - timedelta(seconds = 1), fin, diferencia, 1, e)
        billetera = BilleteraElectronica.objects.get(pk = 1)
        self.assertEqual(billetera.saldo, diferencia)
        
    '''    