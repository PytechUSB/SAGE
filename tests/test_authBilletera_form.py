# -*- coding: utf-8 -*-

from django.test import TestCase
from estacionamientos.forms import authBilleteraForm

class AuthBilleteraFormTestCase(TestCase):
    
    # interior
    def testAuthBilleteraForm(self):
        form_data = {
                     'Pin': '1234',
                     'ID': '1'
        }
        form = authBilleteraForm(data = form_data)
        self.assertTrue(form.is_valid())
    
    # borde
    def testAuthBilletera_FormVacio(self):
        form_data = {}
        form = authBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testAuthBilletera_UnCampoVacio(self):
        form_data = {
            'Pin': '1234',
        }
        form = authBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testAuthBilletera_PinIvalido(self):
        form_data = {
            'Pin': '12345',
            'ID': '1'
        }
        form = authBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    #borde
    def testAuthBilletera_IDIvalido(self):
        form_data = {
            'Pin': '1234',
            'ID': '12345'
        }
        form = authBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testAuthBilletera_DatosInvalidos(self):
        form_data = {
            'Pin': '12345',
            'ID': '12345'
        }
        form = authBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
        
    # malicia
    def testAuthBilletera_EspacioBlanco(self):
        form_data = {
            'Pin': ' ',
            'ID': ' '
        }
        form = authBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())