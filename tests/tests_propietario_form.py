# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import PropietarioForm

###################################################################
#                    ESTACIONAMIENTO_ALL FORM
###################################################################


class PropietarioAllFormTestCase(TestCase):
    
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
    def test_Propietario_invalido_simbolos_especiales(self):
        form_data = {
            'nombres': '#€%! Albeto',
            'apellidos': 'Perez',
            'cedula': '24981045'
        }
        form = PropietarioForm(data = form_data)
        self.assertFalse(form.is_valid())