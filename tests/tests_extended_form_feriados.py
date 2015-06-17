# -*- coding: utf-8 -*-

from django.test import TestCase

from datetime import time

from estacionamientos.models import Propietario,Estacionamiento

from estacionamientos.forms import EstacionamientoExtendedForm,PropietarioForm,EstacionamientoForm,CedulaForm

###################################################################
# ESTACIONAMIENTO_EXTENDED_FORM CON ESQUEMA PARA DIAS FERIADOS
###################################################################

#Dias feriados por default: (dd-mm-yy)
    #2015-05-01
    #2015-06-24
    #2015-07-05
    #2015-07-24
    #2015-10-12
    #2015-12-25

class ExtendedFormDiasFeriadosTestCase(TestCase):

    #########################
    # TDD
    #########################
    def test_estacionamiento_extended_form_feriados(self):
        form_data = { 'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema':'TarifaMinuto',
                      'aceptaFeriados': True,
                      'feriados' : '2015-05-01,2015-06-24'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())
        
    # tdd
    def test_estacionamiento_extended_esquema_dia_feriados_igual(self):
        form_data = { 'puestos': 10,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'feriados' : '2015-05-01,2015-06-24',
                      'esquema':'TarifaHora',
                      'aceptaFeriados': True,
                      'esquemaFeriados':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # tdd
    def test_estacionamiento_extended_esquema_dia_feriados_distinto(self):
        form_data = { 'puestos': 10,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'feriados' : '2015-05-01,2015-06-24',
                      'esquema':'TarifaHora',
                      'aceptaFeriados': True,
                      'esquemaFeriados':'TarifaMinuto'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    #########################
    # BORDES
    #########################

    #hora de inicio de la tarifa especial = hora de apertura
    def test_estacionamiento_extended_form_feriados_incio_igual_apertura(self):
        form_data = { 'horarioin': time(hour = 8,  minute = 0),
                      'horarioout': time(hour = 20,  minute = 50),
                      'esquema':'TarifaHora',
                      'aceptaFeriados': True,
                      'feriados' : '2015-05-01,2015-06-24',
                      'inicioTarifaFeriados': time(hour = 8,  minute = 0),
                      'finTarifaFeriados': time(hour = 11,  minute = 0)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    #hora de finalizacion de la tarifa especial = hora de cierre
    def test_estacionamiento_extended_form_feriados_final_igual_cierre(self):
        form_data = { 'horarioin': time(hour = 8,  minute = 0),
                      'horarioout': time(hour = 20,  minute = 50),
                      'esquema':'TarifaHora',
                      'aceptaFeriados': True,
                      'feriados' : '2015-05-01,2015-06-24',
                      'inicioTarifaFeriados': time( hour = 15,  minute = 0),
                      'finTarifaFeriados': time(hour = 20,  minute = 50)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    #########################
    # ESQUINAS
    #########################

    #hora de inicio de la tarifa especial = hora de apertura y
    #hora de finalizacion  = hora de cierre
    def test_estacionamiento_extended_form_feriados_horarios_iguales(self):
        form_data = { 'horarioin': time(hour = 8,  minute = 0),
                      'horarioout': time(hour = 20,  minute = 50),
                      'esquema':'TarifaHora',
                      'aceptaFeriados': True,
                      'feriados' : '2015-05-01,2015-06-24',
                      'inicioTarifaFeriados': time( hour = 8,  minute = 0),
                      'finTarifaFeriados': time(hour = 20,  minute = 50)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    #########################
    # MALICIA
    #########################

    # esquema feriado inexistente
    def test_estacionamiento_extended_form_esquema_feriado_inexistente(self):
        form_data = { 'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema': 'TarifaHora',
                      'aceptaFeriados': True,
                      'feriados' : '2015-05-01,2015-06-24',
                      'esquemaFeriados': 'TarifaHola'
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # horario de inicio de la tarifa especial mayor al horario de finalizacion de la misma en esquema feriado
    def test_estacionamiento_extended_form_final_menor_inicio_feriado(self):
        form_data = { 'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema': 'TarifaHora',
                      'aceptaFeriados': True,
                      'feriados' : '2015-05-01,2015-06-24',
                      'inicioTarifaFeriados': time( hour = 20,  minute = 0),
                      'finTarifaFeriados': time(hour = 8,  minute = 0)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # hora de finalizacion de tarifa especial mayor a hora de cierre del estacionamiento
    def test_estacionamiento_extended_form_feriados_finalizacion_mayor(self):
        form_data = { 'horarioin': time( hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema': 'TarifaHora',
                      'aceptaFeriados': True,
                      'feriados' : '2015-05-01,2015-06-24',
                      'inicioTarifaFeriados': time( hour = 14,  minute = 0),
                      'finTarifaFeriados': time(hour = 20,  minute = 0)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())

    # hora de inicio de tarifa especial menor a hora de apertura del estacionamiento
    def test_estacionamiento_extended_form_feriados_inicio_menor(self):
        form_data = { 'horarioin': time( hour = 8,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'esquema': 'TarifaHora',
                      'aceptaFeriados': True,
                      'feriados' : '2015-05-01,2015-06-24',
                      'inicioTarifaFeriados': time( hour = 7,  minute = 0),
                      'finTarifaFeriados': time(hour = 12,  minute = 0)
                    }
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertFalse(form.is_valid())