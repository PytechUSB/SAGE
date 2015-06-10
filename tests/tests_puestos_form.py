# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import PuestosForm

###################################################################
#                    PUESTOS FORM
###################################################################


class PuestosFormTestCase(TestCase):    
    
    #tdd
    def test_Un_Campo(self):
        form_data = {
            'particulares': 9
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())
    
    #tdd
    def test_Dos_Campos(self):
        form_data = {
            'particulares': 9,
            'motos'	: 8
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    #tdd
    def test_Tres_Campos(self):
        form_data = {
            'particulares': 9,
            'motos'	: 8,
            'camiones': 2
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())

    #tdd
    def test_Tres_Campos(self):
        form_data = {
            'particulares': 9,
            'motos'	: 8,
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #tdd
    def test_Tres_Campos(self):
        form_data = {
            'particulares': 9,
            'motos'	: 8,
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_Cero_Particulares(self):
        form_data = {
            'particulares': 0,
            'motos'	: 8,
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_Cero_Motos(self):
        form_data = {
            'particulares': 2,
            'motos'	: 0,
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_Cero_Camiones(self):
        form_data = {
            'particulares': 2,
            'motos'	: 3,
            'camiones': 0,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_Cero_Discapacitados(self):
        form_data = {
            'particulares': 2,
            'motos'	: 6,
            'camiones': 2,
            'discapacitados': 0
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_Un_Particular(self):
        form_data = {
            'particulares': 1,
            'motos'	: 8,
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_Una_Moto(self):
        form_data = {
            'particulares': 2,
            'motos'	: 1,
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_Un_Camion(self):
        form_data = {
            'particulares': 2,
            'motos'	: 3,
            'camiones': 1,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #borde
    def test_Un_Discapacitado(self):
        form_data = {
            'particulares': 2,
            'motos'	: 6,
            'camiones': 2,
            'discapacitados': 1
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #esquina
    def test_Ningun_Vehiculo(self):
        form_data = {
            'particulares': 0,
            'motos'	: 0,
            'camiones': 0,
            'discapacitados': 0
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())

    #esquina
    def test_Un_Puesto_Cada_Tipo(self):
        form_data = {
            'particulares': 1,
            'motos'	: 1,
            'camiones': 1,
            'discapacitados': 1
        }
        form = PuestosForm(data = form_data)
        self.assertTrue(form.is_valid())

    #malicia
    def test_Negativo_en_Particulares(self):
        form_data = {
            'particulares': -3,
            'motos'	: 8,
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_Negativo_en_Motos(self):
        form_data = {
            'particulares': 3,
            'motos'	: -8,
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_Negativo_en_Camiones(self):
        form_data = {
            'particulares': 3,
            'motos'	: 8,
            'camiones': -2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_Negativo_en_Discapacitados(self):
        form_data = {
            'particulares': 3,
            'motos'	: 8,
            'camiones': 2,
            'discapacitados': -5
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_String_en_Particulares(self):
        form_data = {
            'particulares': 'hola',
            'motos'	: 8,
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_String_en_Motos(self):
        form_data = {
            'particulares': 3,
            'motos'	: 'hola',
            'camiones': 2,
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_String_en_Camiones(self):
        form_data = {
            'particulares': 3,
            'motos'	: 8,
            'camiones': 'hola',
            'discapacitados': 5
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def test_String_en_Discapacitados(self):
        form_data = {
            'particulares': 3,
            'motos'	: 8,
            'camiones': 2,
            'discapacitados': 'hola'
        }
        form = PuestosForm(data = form_data)
        self.assertFalse(form.is_valid())