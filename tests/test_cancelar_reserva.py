# -*- coding: utf-8 -*-

from django.test import TestCase

from decimal import Decimal
from datetime import (
    datetime,
    time,
    timedelta,
)
from estacionamientos.controller import (
    pago_autenticar, 
    billetera_autenticar
)

from estacionamientos.models import (
    Reserva,
    Pago,
    BilleteraElectronica,
    Recargas,
    Cancelaciones
)

class TestCancelarReserva(TestCase):
    
    def crear_reserva(h_inicio, h_fin):
    
    
    # interno
    def TestCancelarUnaReservacion(self):
        
        
    # borde
    def TestCancelarReservacionBilleteraFull(self):
        
        
    # malicia
    def TestCancelarDosVeces(self):
        
        
    # malicia
    def TestCancelarReservaNoExiste(self):
        
        
    # malicia
    def TestCancelarReservaBilleteraNoExiste(self):
        
        
    # borde
    def TestCancelarReservaAntes(self):
        
        
    # borde
    def TestCancelarReservaDurante(self):
        
    #
















































