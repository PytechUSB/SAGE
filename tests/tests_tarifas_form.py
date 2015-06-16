# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import TarifasForm

###################################################################
#                    TARIFAS FORM
###################################################################


class TarifasFormTestCase(TestCase):  

    #########################
    # TDD
    #########################

    #un solo campo (sin el obligatorio)
    def test_Un_Campo_No_Obligatorio(self):
        form_data = {
            'tarifaFeriados': 9
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #dos campos (sin el obligatorio) 
    def test_Dos_Campos_No_Obligatorios(self):
        form_data = {
            'tarifa2': 10,
            'tarifaFeriados': 9
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #tres campos (sin el obligatorio) 
    def test_Tres_Campos_No_Obligatorios(self):
        form_data = {
            'tarifa2': 20,
            'tarifaFeriados': 9,
            'tarifaFeriados2': 10
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #todos los campos 
    def test_Todos_Los_Campos(self):
        form_data = {
        	'tarifa': 20,
            'tarifa2': 20,
            'tarifaFeriados': 9,
            'tarifaFeriados2': 10
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #########################
    # BORDES
    #########################

    #solo el campo obligatorio
    def test_Un_Campo(self):
        form_data = {
            'tarifa': 9
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #tarifa = 0
    def test_Tarifa_igual_cero(self):
        form_data = {
            'tarifa': 0,
            'tarifa2': 20,
            'tarifaFeriados': 9,
            'tarifaFeriados2': 10
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #tarifa2 = 0
    def test_Tarifa_Especial_igual_cero(self):
        form_data = {
            'tarifa': 20,
            'tarifa2': 0,
            'tarifaFeriados': 9,
            'tarifaFeriados2': 10
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #tarifaFeriados = 0
    def test_Tarifa_Feriada_igual_cero(self):
        form_data = {
            'tarifa': 20,
            'tarifa2': 30,
            'tarifaFeriados': 0,
            'tarifaFeriados2': 10
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #tarifaFeriados2 = 0
    def test_Tarifa_Feriada_Especial_igual_cero(self):
        form_data = {
            'tarifa': 20,
            'tarifa2': 30,
            'tarifaFeriados': 10,
            'tarifaFeriados2': 0
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #########################
    # ESQUINA
    #########################

    #tarifas feriadas iguales a cero
    def test_Tarifas_Feriadas_iguales_cero(self):
        form_data = {
            'tarifa': 20,
            'tarifa2': 30,
            'tarifaFeriados': 0,
            'tarifaFeriados2': 0
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #########################
    # MALICIA
    #########################

    #todas las tarifas igual a cero
    def test_tarifas_iguales_a_cero(self):
        form_data = {
            'tarifa': 0,
            'tarifa2': 0,
            'tarifaFeriados': 0,
            'tarifaFeriados2': 0
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #letras en el primer campo
    def test_tarifa_letras(self):
        form_data = {
            'tarifa': 'hola',
            'tarifa2': 10,
            'tarifaFeriados': 20,
            'tarifaFeriados2': 30
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #letras en el segundo campo
    def test_tarifa2_letras(self):
        form_data = {
            'tarifa': 20,
            'tarifa2': 'hola',
            'tarifaFeriados': 30,
            'tarifaFeriados2': 10
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #letras en el tercer campo
    def test_tarifaFeriados_letras(self):
        form_data = {
            'tarifa': 20,
            'tarifa2': 30,
            'tarifaFeriados': 'hola',
            'tarifaFeriados2': 10
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #letras en el cuarto campo
    def test_tarifaFeriados4_letras(self):
        form_data = {
            'tarifa': 20,
            'tarifa2': 30,
            'tarifaFeriados': 10,
            'tarifaFeriados2': 'hola'
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())