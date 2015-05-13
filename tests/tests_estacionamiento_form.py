# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import EstacionamientoForm
from estacionamientos.models import Propietario

###################################################################
#                    ESTACIONAMIENTO_ALL FORM
###################################################################


class EstacionamientoAllFormTestCase(TestCase):
    
    
    # malicia
    def test_campos_vacios(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {}
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_solo_un_campo_necesario(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_dos_campos_necesarios(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id,
            'nombre': 'Orinoco'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_tres_campos_necesarios(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id,
            'nombre': 'Orinoco',
            'direccion': 'Caracas'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_todos_los_campos_necesarios(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id,
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertTrue(form.is_valid())

    # caso borde
    def test_RIF_tamano_invalido(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id,
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-1234567'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_RIF_formato_invalido(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'Kaa123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_agregar_telefonos(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id,
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '02129322878',
            'telefono_2': '04149322878',
            'telefono_3': '04129322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_formato_invalido_telefono(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id,
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '02193228782'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # caso borde
    def test_tamano_invalido_telefono(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id,
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '0212322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())

    # malicia
    def test_agregar_correos_electronicos(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id,
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '02129322878',
            'telefono_2': '04149322878',
            'telefono_3': '04129322878',
            'email_1': 'adminsitrador@admin.com',
            'email_2': 'usua_rio@users.com'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertTrue(form.is_valid())

    # malicia
    def test_correo_electronico_invalido(self):
        prop=Propietario(nombres="Pedro",apellidos="Perez",cedula="19345678")
        prop.save()
        form_data = {
            'propietario': prop.id,
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V-123456789',
            'telefono_1': '02129322878',
            'telefono_2': '04149322878',
            'telefono_3': '04129322878',
            'email_1': 'adminsitrador@a@dmin.com'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertFalse(form.is_valid())
