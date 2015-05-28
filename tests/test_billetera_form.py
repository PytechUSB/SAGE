# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import BilleteraForm

###################################################################
#                    CREAR-BILLETERA FORM
###################################################################

class CrearBilleteraFormTestCase(TestCase):

    # malicia
    def testCrearBilleteraForm_Vacio(self):
        form_data = {}
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testCrearBilleteraForm_UnCampo(self):
        form_data = {
            'nombre': 'Andrea'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
    
    # borde    
    def testCrearBilleteraForm_DosCampos(self):
        form_data = {
            'nombre': 'Neo',
            'apellido': 'Noria'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
     
    # borde   
    def testCrearBilleteraForm_TresCampos(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Perez',
            'cedula': '12345678'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde    
    def testCrearBilleteraForm_CuatroCampos(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Perez',
            'cedula': '12345678',
            'PIN': '1234'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde    
    def testCrearBilleteraForm_CincoCampos(self):
        form_data = {
            'nombre': 'Carlos',
            'apellido': 'Perez',
            'cedula': '12345678',
            'PIN': '1234',
            'cedulaTipo': 'V'
        }
        form = BilleteraForm(data = form_data)
        self.assertTrue(form.is_valid())
    
    # borde    
    def testBilleteraForm_NombreInvalidoDigitos(self):
        form_data = {    
            'nombre': 'Jose1',
            'apellido': 'Perez',
            'cedula': '12345678',
            'PIN': '1234',
            'cedulaTipo': 'V',
            'identificador': '1000100010001000'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testBilleteraForm_NombreInvalidoEspacio(self):
        form_data = {    
            'nombre': ' Jose',
            'apellido': 'Perez',
            'cedula': '12345678',
            'cedulaTipo': 'V',
            'PIN': '1234',
            'identificador': '1000100010001000'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testBilleteraForm_NombreInvalidoSimbolos(self):
        form_data = {    
            'nombre': 'Jose .',
            'apellido': 'Perez',
            'cedula': '12345678',
            'cedulaTipo': 'V',
            'PIN': '1234',
            'identificador': '1000100010001000'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
    
    # borde    
    def testBilleteraForm_ApellidoInvalidoDigitos(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez Martinez1',
            'cedula': '12345678',
            'cedulaTipo': 'V',
            'PIN': '1234',
            'identificador': '1000100010001000'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde    
    def testBilleteraForm_ApellidoInvalidoEspacio(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': ' Perez Martinez',
            'cedulaTipo': 'V',
            'cedula': '12345678',
            'PIN': '1234',
            'identificador': '1000100010001000'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde    
    def testBilleteraForm_ApellidoInvalidoSimbolos(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez@ Martinez',
            'cedula': '12345678',
            'cedulaTipo': 'V',
            'PIN': '1234',
            'identificador': '1000100010001000'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde    
    def testBilleteraForm_CedulaInvalida(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez Martinez',
            'cedula': 'V12345678',
            'cedulaTipo': 'V',
            'PIN': '1234',
            'identificador': '1000100010001000'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde    
    def testBilleteraForm_CedulaLimiteInferior(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez Martinez',
            'cedula': '0',
            'cedulaTipo': 'V',
            'PIN': '1234',
            'identificador': '1000100010001000'
        }
        form = BilleteraForm(data = form_data)
        self.assertTrue(form.is_valid())
        
    # borde    
    def testBilleteraForm_CedulaLimiteSuperior(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez Martinez',
            'cedula': '999999999',
            'cedulaTipo': 'V',
            'PIN': '1234',
            'identificador': '1000100010001000'
        }
        form = BilleteraForm(data = form_data)
        self.assertTrue(form.is_valid())
        
    # borde
    def testBilleteraForm_PINTamañoInvalido(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez Martinez',
            'cedula': '12345678',
            'cedulaTipo': 'V',
            'PIN': '12345',
            'identificador': '9999999999999999'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testBilleteraForm_PINInvalido(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez Martinez',
            'cedula': '12345678',
            'cedulaTipo': 'V',
            'PIN': 'P123',
            'identificador': '9999999999999999'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def testBilleteraForm_PINInvalidoEspacio(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez Martinez',
            'cedula': '12345678',
            'cedulaTipo': 'V',
            'PIN': '12 34',
            'identificador': '9999999999999999'
        }
        form = BilleteraForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # borde
    def testBilleteraForm_PINLimiteInferior(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez Martinez',
            'cedula': '12345678',
            'cedulaTipo': 'V',
            'PIN': '0000',
            'identificador': '9999999999999999'
        }
        form = BilleteraForm(data = form_data)
        self.assertTrue(form.is_valid())
        
    # borde
    def testBilleteraForm_PINLimiteSuperior(self):
        form_data = {    
            'nombre': 'Jose',
            'apellido': 'Perez Martinez',
            'cedula': '12345678',
            'cedulaTipo': 'V',
            'PIN': '9999',
            'identificador': '9999999999999999'
        }
        form = BilleteraForm(data = form_data)
        self.assertTrue(form.is_valid())
