# -*- coding: utf-8 -*-

from django.test import TestCase
from estacionamientos.forms import cambioPinBilleteraForm

class CambioPinFormTestCase(TestCase):
    
    # interiror
    def testCambioPinForm(self):
        form_data = {
                    'Pin': '2222',
                    'nuevo_Pin1': '1111',
                    'nuevo_Pin2': '1111'
        }
        form = cambioPinBilleteraForm(data = form_data)
        self.assertTrue(form.is_valid())
                        
    # malicia
    def testCambioPin_FormVacio(self):
        form_data = {}
        form = cambioPinBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testCambioPin_UnCampoVacio(self):
        form_data = {
            'Pin': '1111',
            'nuevo_Pin1': '1111'
        }
        form = cambioPinBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testCambioPin_PINInvalido(self):
        form_data = {
           'Pin': 'aaaa',
            'nuevo_Pin1': '1111',
            'nuevo_Pin2': '1111'
        }
        form = cambioPinBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())   
        
    #borde
    def testCambioPin_nuevo_Pin1Invalido(self):
        form_data = {
            'Pin': '1111',
            'nuevo_Pin1': 'qqqq',
            'nuevo_Pin2': '1111'
        }
        form = cambioPinBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    #borde
    def testCambioPin_nuevo_Pin2Invalido(self):
        form_data = {
            'Pin': '1111',
            'nuevo_Pin1': '1111',
            'nuevo_Pin2': 'qqqq'
        }
        form = cambioPinBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())    
        
    # borde
    def testCambioPin_DatosInvalidos(self):
        form_data = {
            'Pin': 'qqqq',
            'nuevo_Pin1': 'qqqq',
            'nuevo_Pin2': 'qqqq'
        }
        form = cambioPinBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    
    # malicia
    def testCambioPin_CamposNulos(self):
        form_data = {
            'Pin': '',
            'nuevo_Pin1': '',
            'nuevo_Pin2': ''
        }
        form = cambioPinBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def testCambioPin_EspacioBlanco(self):
        form_data = {
            'Pin': '  ',
            'nuevo_Pin1': '1111',
            'nuevo_Pin2': '  '
        }
        form = cambioPinBilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())