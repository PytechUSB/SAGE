# -*- coding: utf-8 -*-

from django.test import TestCase
from estacionamientos.forms import AdministrarSAGEForm

class AdministrarSAGEFormTestCase(TestCase):
    # interior
    def testAdministrarSAGEForm(self):
        form_data = {
                     'porcentaje': '0.5'
        }
        form = AdministrarSAGEForm(data = form_data)
        self.assertTrue(form.is_valid())
    
    # borde
    def testAdministrarSAGEForm_minimo(self):
        form_data = {
                     'porcentaje': '0.0'
        }
        form = AdministrarSAGEForm(data = form_data)
        self.assertTrue(form.is_valid())
    
    # borde
    def testAdministrarSAGEForm_maximo(self):
        form_data = {
                     'porcentaje': '9.9'
        }
        form = AdministrarSAGEForm(data = form_data)
        self.assertTrue(form.is_valid())
    
    # malicia
    def testAdministrarSAGEForm_negativo(self):
        form_data = {
                     'porcentaje': -0.5
        }
        form = AdministrarSAGEForm(data = form_data)
        self.assertFalse(form.is_valid())
    
    
    # malicia
    def testAdministrarSAGE_FormVacio(self):
        form_data = {}
        form = AdministrarSAGEForm(data = form_data)
        self.assertFalse(form.is_valid())
    

    #borde
    def testAdministrarSAGE_PorcentajeInvalido(self):
        form_data = {
            'porcentaje': '10.0'
        }
        form = AdministrarSAGEForm(data = form_data)
        self.assertFalse(form.is_valid())
           
    
    # malicia
    def testAdministrarSAGE_CampoNulo(self):
        form_data = {
            'porcentaje': ''
        }
        form = AdministrarSAGEForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def testAdministrarSAGE_EspacioBlanco(self):
        form_data = {
            'porcentaje': ' '
        }
        form = AdministrarSAGEForm(data = form_data)
        self.assertFalse(form.is_valid())