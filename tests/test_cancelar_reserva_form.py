# -*- coding: utf-8 -*-

from django.test import TestCase
from estacionamientos.forms import CancelaReservaForm

class CancelaReservaFormTestCase(TestCase):
    
    # interiror
    def testCancelaReservaForm(self):
        form_data = {
                    'ID': '1',
                    'cedulaTipo': 'V',
                    'cedula': '1'
        }
        form = CancelaReservaForm(data = form_data)
        self.assertTrue(form.is_valid())
                        
    # malicia
    def testCancelaReserva_FormVacio(self):
        form_data = {}
        form = CancelaReservaForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testCancelaReserva_UnCampoVacio(self):
        form_data = {
            'ID': '1',
            'cedulaTipo': 'E'
        }
        form = CancelaReservaForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testCancelaReserva_IDInvalido(self):
        form_data = {
            'ID': 'a',
            'cedulaTipo': 'V',
            'cedula':'1'
        }
        form = CancelaReservaForm(data = form_data)
        self.assertFalse(form.is_valid())   
        
    #borde
    def testCancelaReserva_CedulaInvalida(self):
        form_data = {
            'ID': '12',
            'cedulaTipo': 'V',
            'cedula': 'abc1'
        }
        form = CancelaReservaForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testCancelaReserva_DatosInvalidos(self):
        form_data = {
            'ID': '12e45',
            'cedulaTipo': 'E',
            'cedula':'1123d4'
        }
        form = CancelaReservaForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    
    # malicia
    def testCancelaReserva_CamposNulos(self):
        form_data = {
            'ID': '',
            'cedulaTipo': '',
            'cedula': ''
        }
        form = CancelaReservaForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def testCancelaReserva_EspacioBlanco(self):
        form_data = {
            'ID': ' ',
            'cedulaTipo': 'V',
            'cedula': ' '
        }
        form = CancelaReservaForm(data = form_data)
        self.assertFalse(form.is_valid())