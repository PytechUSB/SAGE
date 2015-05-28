# -*- coding: utf-8 -*-

from django.test import TestCase
from estacionamientos.forms import BilleteraPagoForm

class BilleteraBilleteraPagoFormTestCase(TestCase):
    
    # interno
    def testBilleteraPago_FormValido(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '12345678',
            'monto': '20',
            'tarjeta': '1234567890123456',
            'tarjetaTipo':'Vista'
        } 
        form = BilleteraPagoForm(data = form_data)
        self.assertTrue(form.is_valid())
    
    # borde
    def testBilleteraPago_CamposVacios(self):
        form_data = {}
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # borde
    def testBilleteraPago_UnCampo(self):
        form_data = {
            'nombre': 'Maria',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testBilleteraPago_DosCampos(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testBilleteraPago_TresCampos(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testBilleteraPago_CuatroCampos(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '12345678',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testBilleteraPago_CincoCampos(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '12345678',
            'tarjetaTipo': 'Vista',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testBilleteraPago_NombreInvalido(self):
        form_data = {
            'nombre': 'Maria1',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '12345678',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    #borde
    def testBilleteraPago_NombreEspacio(self):
        form_data = {
            'nombre': ' Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '12345678',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testBilleteraPago_ApellidoInvalido(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez1',
            'cedulaTipo': 'V',
            'cedula': '12345678',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

       
    #borde
    def testBilleteraPago_ApellidoEspacio(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': ' Perez',
            'cedulaTipo': 'V',
            'cedula': '12345678',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testBilleteraPago_CedulaTipoInvalido(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'J',
            'cedula': '12345678',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testBilleteraPago_CedulaInvalida(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': 'V 123',
            'tarjetaTipo': 'Vista',
            'tarjeta': '1234567890123456',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())
        

    #borde
    def testBilleteraPago_TipoTarjetaInvalido(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '12345678',
            'tarjetaTipo': 'VISA',
            'tarjeta': '0123456789012345',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #borde
    def testBilleteraPago_TarjetaInvalido(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': '12345678',
            'tarjetaTipo': 'Vista',
            'tarjeta': 'a1234',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def testBilleteraPago_DosCamposInvalidos(self):
        form_data = {
            'nombre': 'Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'T',
            'cedula': '12345678',
            'tarjetaTipo': 'Vista',
            'tarjeta': 'a1234',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def testBilleteraPago_CuatroCamposInvalidos(self):
        form_data = {
            'nombre': ' Maria',
            'apellido': 'Perez',
            'cedulaTipo': 'V',
            'cedula': 'a1234567',
            'tarjetaTipo': 'Vista',
            'tarjeta': '0123456789012345',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())

    #malicia
    def testBilleteraPago_CamposInvalidos(self):
        form_data = {
            'nombre': ' Maria',
            'apellido': '1Perez',
            'cedulaTipo': 'T',
            'cedula': 'a1234567',
            'tarjetaTipo': 'VISA',
            'tarjeta': 'a1234',
        }
        form = BilleteraPagoForm(data = form_data)
        self.assertFalse(form.is_valid())