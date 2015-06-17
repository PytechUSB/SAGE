# -*- coding: utf-8 -*-

from django.test import TestCase

from decimal import Decimal

from datetime import timedelta, time

from estacionamientos.models import (
    Pago,
    Cancelaciones,
    BilleteraElectronica, 
    Propietario, 
    Estacionamiento,
    Reserva,
    AdministracionSage
)
from estacionamientos.controller import (
    asigna_id_unico,
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
    
def crear_factura(_reserva, monto, tarjetaTipo, facturaMovida):
    pago = Pago(
            reserva = _reserva,
            id = asigna_id_unico(),
            fechaTransaccion = datetime.now(),
            cedula = "10",
            cedulaTipo = "V",
            tarjetaTipo = tarjetaTipo,
            monto = Decimal(monto),
            facturaMovida = facturaMovida
    )
    pago.save()
    
def crear_pago(h_inicio, h_fin, monto, estacionamiento, tarjetaTipo, facturaMovida = None):
    r = crear_reserva(h_inicio, h_fin, estacionamiento)
    crear_factura(r, monto, tarjetaTipo, facturaMovida)
    
def pago_mover_reserva(idPagoAMover, h_inicio, h_fin, diferencia, estacionamiento, tarjetaTipo):
    pagoAnterior = Pago.objects.get(pk = idPagoAMover)
    crear_pago(h_inicio, h_fin, pagoAnterior.monto + diferencia, estacionamiento, tarjetaTipo, pagoAnterior)
    cancelacion = Cancelaciones(
        id = asigna_id_unico(),
        pagoCancelado = pagoAnterior,
        monto = 0,
        fechaTransaccion = datetime.now()    
    )
    cancelacion.save()
    pagoAnterior.fue_movido()
    
def recarga_mover_reserva(idPagoAMover, h_inicio, h_fin, diferencia, id_billetera, estacionamiento, tarjetaTipo):
    pagoAnterior = Pago.objects.get(pk = idPagoAMover)
    administracion = AdministracionSage.objects.get(pk = 1)
    nuevo_monto = pagoAnterior.monto - diferencia
    if pagoAnterior.tarjetaTipo != 'Billetera Electronica':
        monto_debitar = administracion.calcular_monto(nuevo_monto)
    else:
        if pagoAnterior.facturaMovida != None:
            monto_debitar = administracion.calcular_monto(nuevo_monto)
        else:
            monto_debitar = 0
    billetera = BilleteraElectronica.objects.get(pk = id_billetera)
    montoARecargar = diferencia
    crear_pago(h_inicio, h_fin, pagoAnterior.monto - montoARecargar, estacionamiento, tarjetaTipo, pagoAnterior)
    cancelacion = Cancelaciones(
        id = asigna_id_unico(),
        pagoCancelado = pagoAnterior,
        billetera = billetera,
        monto = montoARecargar,
        fechaTransaccion = datetime.now()    
    )
    cancelacion.save()
    pagoAnterior.fue_movido()
    billetera.recargar_saldo(montoARecargar - monto_debitar)

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
                
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
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
            monto_debitar = administracion.calcular_monto(nuevo_monto)
        else:
            if pago.facturaMovida != None:
                monto_debitar = administracion.calcular_monto(nuevo_monto)
            else:
                monto_debitar = 0

        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, diferencia, e, tarjetaTipo)
        pago = Pago.objects.get(pk = 2)
        self.assertTrue(pago.monto == monto + diferencia and monto_debitar == Decimal('9.9'))
    
    # interior    
    def testMoverReservaMontoMenor(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Vista'
        p = crear_propietario()
        e = crear_estacionamiento(p, 168)
        monto = 100
        diferencia = Decimal('90')
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        crear_pago(inicio, fin, monto, e, tarjetaTipo)
        crear_billetera()
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            recarga_mover_reserva(1, inicio, fin, diferencia, 1, e, tarjetaTipo)
        billetera = BilleteraElectronica.objects.get(pk = 1)
        self.assertEqual(billetera.saldo, Decimal('90') - Decimal('.99'))
    
    
    # interno  
    def testMoverReservaMasDeUnaVezBilletera(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Billetera Electronica'
        p = crear_propietario()
        e = crear_estacionamiento(p, 168)
        monto = Decimal(10)
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        crear_pago(inicio, fin, monto, e, tarjetaTipo)
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, 0, e, tarjetaTipo)
            
        pago = Pago.objects.get(pk = 2)
        administracion = AdministracionSage.objects.get(pk = 1)
        if pago.tarjetaTipo != 'Billetera Electronica':
            monto_debitar = administracion.calcular_monto(100)
        else:
            if pago.facturaMovida != None:
                monto_debitar = administracion.calcular_monto(100)
            else:
                monto_debitar = 0    
            
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(2, inicio, fin, 90, e, tarjetaTipo)
            
        pago = Pago.objects.get(pk = 4)    
        self.assertTrue(pago.monto == 100 and monto_debitar == Decimal('9.9'))
        
    # interno  
    def testMoverReservaMasDeUnaVezCredito(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Vista'
        p = crear_propietario()
        e = crear_estacionamiento(p, 168)
        monto = Decimal(10)
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        crear_pago(inicio, fin, monto, e, tarjetaTipo)
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, 0, e, tarjetaTipo)
            
        pago = Pago.objects.get(pk = 2)
        administracion = AdministracionSage.objects.get(pk = 1)
        if pago.tarjetaTipo != 'Billetera Electronica':
            monto_debitar = administracion.calcular_monto(100)
        else:
            if pago.facturaMovida != None:
                monto_debitar = administracion.calcular_monto(100)
            else:
                monto_debitar = 0    
            
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(2, inicio, fin, 90, e, tarjetaTipo)
            
        pago = Pago.objects.get(pk = 4)    
        self.assertTrue(pago.monto == 100 and monto_debitar == Decimal('9.9'))
        
    # borde
    def testMoverReservaValidaCambioHorizonte(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Billetera Electronica'
        p = crear_propietario()
        e = crear_estacionamiento(p, 48)
        inicio = datetime.now()
        fin = datetime.now() + timedelta(days = 4)
        crear_pago(inicio, fin, Decimal('0.01'), e, tarjetaTipo)
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, 0, e, tarjetaTipo)
        pagos = Pago.objects.all()
        self.assertTrue(len(pagos) == 2)
        
    # borde
    def testMoverReservaInvalidaCambioHorizonte(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Billetera Electronica'
        p = crear_propietario()
        e = crear_estacionamiento(p, 48)
        inicio = datetime.now() + timedelta(hours = 1)
        fin = datetime.now() + timedelta(days = 4)
        crear_pago(inicio, fin, Decimal('0.01'), e, tarjetaTipo)
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, 0, e, tarjetaTipo)
        pagos = Pago.objects.all()
        self.assertTrue(len(pagos) == 1)
        
    # borde
    def testMoverReservaFueraHorizonte(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Billetera Electronica'
        p = crear_propietario()
        e = crear_estacionamiento(p, 48)
        inicio = datetime.now() + timedelta(days = 1, hours = 1)
        fin = datetime.now() + timedelta(days = 4)
        crear_pago(inicio, fin, Decimal('0.01'), e, tarjetaTipo)
        e.horizonte = 24
        e.save()
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, 0, e, tarjetaTipo)
        pagos = Pago.objects.all()
        self.assertTrue(len(pagos) == 1)
        
    # borde
    def testMoverReservaHorizonteCero(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Billetera Electronica'
        p = crear_propietario()
        e = crear_estacionamiento(p, 48)
        inicio = datetime.now() + timedelta(days = 1, hours = 1)
        fin = datetime.now() + timedelta(days = 4)
        crear_pago(inicio, fin, Decimal('0.01'), e, tarjetaTipo)
        e.horizonte = 0
        e.save()
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, 0, e, tarjetaTipo)
        pagos = Pago.objects.all()
        self.assertTrue(len(pagos) == 1)
        
    # borde
    def testMoverReservaHorizonteMaximo(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Billetera Electronica'
        p = crear_propietario()
        e = crear_estacionamiento(p, 336)
        inicio = datetime.now()
        fin = datetime.now() + timedelta(days = 14)
        crear_pago(inicio, fin, Decimal('0.01'), e, tarjetaTipo)
        nuevo_inicio = datetime.now()
        nuevo_fin = datetime.now() + timedelta(hours = 336)
        if (validarHorarioReservaMover(inicio, fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, 0, e, tarjetaTipo)
        pagos = Pago.objects.all()
        self.assertTrue(len(pagos) == 2)
        
    # borde
    def testMoverReservaInvalidaHorizonteMaximo(self):
        AdministracionSage.objects.create_AdministracionSage(9.9)
        tarjetaTipo = 'Billetera Electronica'
        p = crear_propietario()
        e = crear_estacionamiento(p, 336)
        inicio = datetime.now()
        fin = inicio + timedelta(days = 15)
        crear_pago(inicio, fin, Decimal('0.01'), e, tarjetaTipo)
        nuevo_inicio = datetime.now() + timedelta(hours = 1)
        nuevo_fin = nuevo_inicio + timedelta(days = 15)
        if (validarHorarioReservaMover(nuevo_inicio, nuevo_fin, e.apertura, e.cierre, e.horizonte)[0] and
            (marzullo(1, inicio, fin, 'Particular', 1))):
            pago_mover_reserva(1, inicio, fin, 0, e, tarjetaTipo)
        pagos = Pago.objects.all()
        self.assertTrue(len(pagos) == 1)
        
    