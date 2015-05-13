# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import PropietarioForm

###################################################################
#                    ESTACIONAMIENTO_ALL FORM
###################################################################


class PropietarioAllFormTestCase(TestCase):
    
    # caso borde
    def test_Propietario_nombres_vacio(self):
        form_data = {
            'nombres': '',
            'apellidos': 'Perez',
            'cedula': '24981045'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # caso borde
    def test_Propietario_apellidos_vacio(self):
        form_data = {
            'nombres': 'Carlos',
            'apellidos': '',
            'cedula': '24981045'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # caso borde
    def test_Propietario_cedula_vacio(self):
        form_data = {
            'nombres': 'Carlos',
            'apellidos': 'Perez',
            'cedula': ''
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def test_Propietario_invalido_digitos_en_campo(self):
        form_data = {
            'nombres': '12345',
            'apellidos': 'Perez',
            'cedula': '24981045'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_Propietario_invalido_campo_cedula(self):
        form_data = {
            'nombres': '12345',
            'apellidos': 'Perez',
            'cedula': '2A-981045'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def test_Propietario_invalido_simbolos_especiales(self):
        form_data = {
            'nombres': '#€%! Albeto',
            'apellidos': 'Perez',
            'cedula': '24981045'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())