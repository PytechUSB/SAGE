# -*- coding: utf-8 -*-

from django.test import TestCase

from datetime import time

from estacionamientos.forms import EstacionamientoExtendedForm

###################################################################
# ESTACIONAMIENTO_EXTENDED_FORM
###################################################################

class ExtendedFormTestCase(TestCase):

    #########################
    # TDD
    #########################

    #un solo campo obligatorio
    def test_estacionamiento_extended_form_un_campo(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    #dos campos obligatorios
    def test_estacionamiento_extended_form_dos_campos(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    #########################
    # BORDES
    #########################

    # todos los campos obligatorios
    def test_estacionamiento_extended_form_todos_campos_bien(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # hora de apertura = 00:00
    def test_estacionamiento_extended_form_apertura_00(self):
        form_data = { 'horarioin': time(hour = 0,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # hora de cierre = 11:59
    def test_estacionamiento_extended_form_cierre_11_59(self):
        form_data = { 'horarioin': time(hour = 8,  minute = 0),
                      'horarioout': time(hour = 11,  minute = 59),
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # hora de apertura del estacionamiento igual a la hora de cierre
    def test_estacionamiento_extended_form_hora_inicio_igual_hora_cierre(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 6,  minute = 0),
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    #########################
    # MALICIA
    #########################

    # string en la hora de apertura
    def test_estacionamiento_extended_form_string_hora_inicio(self):
        form_data = { 'horarioin': 'holaa',
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # string en la hora de cierre
    def test_estacionamiento_extended_form_string_hora_cierre(self):
        form_data = { 'horarioin': time(hour = 19,  minute = 0),
                      'horarioout': 'holaa',
                      'esquema':'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # esquema tarifario inexistente
    def test_estacionamiento_extended_form_esquema_inexistente(self):
        form_data = { 'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema': 'TarifaHola'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # horario de cierre menor al de la apertura del estacionamiento
    def test_estacionamiento_extended_form_cierre_menor_apertura(self):
        form_data = { 'horarioin': time( hour = 20,  minute = 0),
                      'horarioout': time(hour = 8,  minute = 0),
                      'esquema': 'TarifaHora'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # horario de inicio de la tarifa especial mayor al horario de finalizacion de la misma
    def test_estacionamiento_extended_form_final_menor_inicio(self):
        form_data = { 'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema': 'TarifaHora',
                      'inicioTarifa2': time( hour = 20,  minute = 0),
                      'finTarifa2': time(hour = 8,  minute = 0)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # hora de finalizacion de tarifa especial mayor a hora de cierre del estacionamiento
    def test_estacionamiento_extended_form_hora_finalizacion_mayor(self):
        form_data = { 'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema': 'TarifaHora',
                      'inicioTarifa2': time( hour = 14,  minute = 0),
                      'finTarifa2': time(hour = 18,  minute = 0)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # hora de inicio de tarifa especial menor a hora de apertura del estacionamiento
    def test_estacionamiento_extended_form_hora_inicio_menor(self):
        form_data = { 'horarioin': time( hour = 8,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema': 'TarifaHora',
                      'inicioTarifa2': time( hour = 7,  minute = 0),
                      'finTarifa2': time(hour = 12,  minute = 0)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())