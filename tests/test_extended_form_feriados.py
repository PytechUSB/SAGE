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

    # tdd
    def test_estacionamiento_extended_esquema_dia_feriados_igual(self):
        form_data = { 'puestos': 10,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora',
                      'esquemaFeriados':'TarifaHora'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())

    # tdd
    def test_estacionamiento_extended_esquema_dia_feriados_distinto(self):
        form_data = { 'puestos': 10,
                      'horarioin': time(hour = 6,  minute = 0),
                      'horarioout': time(hour = 19,  minute = 0),
                      'tarifa': '12',
                      'esquema':'TarifaHora',
                      'esquemaFeriados':'TarifaMinuto'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertTrue(form.is_valid())