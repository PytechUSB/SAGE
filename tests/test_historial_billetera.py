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
, asigna_id_unico, buscar_historial_billetera)

from estacionamientos.models import (
    Reserva,
    Pago,
    BilleteraElectronica,
    Recargas,
    Cancelaciones,
    Propietario,
    Estacionamiento)
from idlelib.IdleHistory import History

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
            tarjetaTipo = "Billetera Electronica",
            nombreUsuario = 'Maria',
            apellidoUsuario = 'Perez',
            idBilletera = '1',
            monto = Decimal(monto)
    )
    pago.save()
    
def crear_pago(h_inicio, h_fin, monto, p):
    e = crear_estacionamiento(p)
    r = crear_reserva(h_inicio, h_fin, e)
    crear_factura(r, monto)


def cancelar_reservacion(id_pago, id_billetera, tiempo = datetime.now() + timedelta(seconds = 60)):
    try:
        pago = Pago.objects.get(pk = id_pago)
        _billetera = BilleteraElectronica.objects.get(pk = id_billetera)
        if ((pago.validar_cancelacion(tiempo)) and 
            (_billetera.validar_recarga(pago.monto))):
            c = Cancelaciones(
                  pagoCancelado = pago,
                  billetera = _billetera,
                  id = asigna_id_unico(),
                  monto = pago.monto,
                  fechaTransaccion = datetime.now()            
            )
            pago.cancelar_reserva()
            _billetera.recargar_saldo(pago.monto)
            c.save()
    except:
        pass
        
def crear_recarga(billetera, numTarjeta, monto):
    billetera = BilleteraElectronica.objects.get(pk = billetera)
    recarga = Recargas(
                id = asigna_id_unico(),
                fechaTransaccion = datetime.now(),
                cedulaTipo = 'V',
                cedula = '12345678',
                tarjetaTipo = 'Vista',
                monto = monto,
                billetera = billetera,
                numTarjeta = numTarjeta
    ) 
    recarga.save()
  
class TestHistorialBilletera(TestCase):
    
    #interior
    def testHistorialBilletera(self):
        crear_billetera(0)
        historial = buscar_historial_billetera(1)
        self.assertEqual(historial, [])
        
    # interior
    def testHistorialRecarga(self):
        crear_billetera(0)
        crear_recarga(1, '1234567812345678', 5000)
        historial = buscar_historial_billetera(1)
        recarga = Recargas.objects.get(pk = 1)
        self.assertTrue(len(historial) == 1 and historial[0] == recarga)
        
    # interior    
    def testHistorialDosBilleteras(self):
        crear_billetera(0) 
        crear_billetera(0)
        crear_recarga(1, '1234567812345678', 5000)
        crear_recarga(2, '1234567812345678', 2000)
        historial = buscar_historial_billetera(1)
        recarga1 = Recargas.objects.get(pk = 1)
        self.assertTrue(len(historial) == 1 and historial[0] == recarga1)
        
    def testHistorialPagoCancelacionRecarga(self):
        crear_billetera(0)
        crear_recarga(1, '1234567812345678', 1000)
        recarga = Recargas.objects.get(pk = 1)
        inicio = datetime.now() + timedelta(days = 1)
        fin = datetime.now() + timedelta(days = 1, hours = 1)
        p = crear_propietario()
        crear_pago(inicio, fin, 10, p)
        pago1 = Pago.objects.get(pk = 2)
        inicio1 = datetime.now() + timedelta(days = 2)
        fin1 = datetime.now() + timedelta(days = 2, hours = 2)
        crear_pago(inicio1, fin1, 30, p)
        pago2 = Pago.objects.get(pk = 3)
        cancelar_reservacion(2, 1)
        cancelacion = Cancelaciones.objects.get(pk = 4)
        historial = buscar_historial_billetera(1)
        self.assertTrue(len(historial) == 4 and historial[0] == recarga and 
                        historial[1] == pago1 and historial[2] == pago2 and
                        historial[3] == cancelacion)