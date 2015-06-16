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
            'tarifa2': 9
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #todos los campos 
    def test_Todos_Los_Campos(self):
        form_data = {
        	'tarifa': 20,
            'tarifa2': 10
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
            'tarifa2': 20
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #tarifa2 = 0
    def test_Tarifa_Especial_igual_cero(self):
        form_data = {
            'tarifa': 20,
            'tarifa2': 0
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #########################
    # ESQUINA
    #########################

    #tarifas feriadas iguales a cero
    def test_Tarifas_iguales_cero(self):
        form_data = {
            'tarifa': 0,
            'tarifa2': 0
        }
        form = TarifasForm(data = form_data)
        self.assertTrue(form.is_valid())

    #########################
    # MALICIA
    #########################

    #letras en el primer campo
    def test_tarifa_letras(self):
        form_data = {
            'tarifa': 'hola',
            'tarifa2': 10
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #letras en el segundo campo
    def test_tarifa2_letras(self):
        form_data = {
            'tarifa': 20,
            'tarifa2': 'hola'
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #numeros negativos en el primer campo
    def test_tarifa_negativo(self):
        form_data = {
            'tarifa': -2,
            'tarifa2': 10
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())

    #numeros negativos en el segundo campo
    def test_tarifa2_negativo(self):
        form_data = {
            'tarifa': 2,
            'tarifa2': -10
        }
        form = TarifasForm(data = form_data)
        self.assertFalse(form.is_valid())