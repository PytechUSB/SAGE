# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.models import BilleteraElectronica

###################################################################
# TESTS DE CAMBIO DE PIN
###################################################################

class CambioPin(TestCase):

    #test de pin errado
    def test_pin_errado(self):
            billetera1 = BilleteraElectronica()
            billetera1.id = 1
            billetera1.PIN = 1234
            billetera1.cambiar_pin(1111, 2222, 2222)
            
            self.assertEqual(billetera1.PIN,1234)
    
    #test de los nuevos pin diferentes        
    def test_pin_nuevos_diferentes(self):
            billetera1 = BilleteraElectronica()
            billetera1.id = 1
            billetera1.PIN = 1234
            billetera1.cambiar_pin(1234, 2222, 1111)
            
            self.assertEqual(billetera1.PIN,1234)        
    
    #test de cambio de pin
    def test_pin_cambiado(self):
            billetera1 = BilleteraElectronica()
            billetera1.id = 1
            billetera1.PIN = 1234
            billetera1.cambiar_pin(1234, 2222, 2222)
            
            self.assertEqual(billetera1.PIN,2222)