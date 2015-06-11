# -*- coding: utf-8 -*-

from django.test import TestCase

from datetime import time

from estacionamientos.forms import EstacionamientoExtendedForm

###################################################################
# ESTACIONAMIENTO_EXTENDED_FORM
###################################################################

class ExtendedFormTestCase(TestCase):

    # malicia
    def test_estacionamiento_extended_form_un_campo(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_dos_campos(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_tres_campos(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde | todos los campos obligatorios
    def test_estacionamiento_extended_form_todos_campos_bien(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # caso borde
    def test_estacionamiento_extended_form_hora_inicio_igual_hora_cierre(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 6,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_string_hora_inicio(self):
        form_data = { 'horarioin': 'holaa',
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_estacionamiento_extended_form_none_en_tarifa(self):
        form_data = { 'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': None,
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())