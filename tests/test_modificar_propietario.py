# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import PropietarioForm,EstacionamientoForm,CedulaForm

from estacionamientos.models import Propietario,Estacionamiento

from django.db import transaction

from django.db.utils import IntegrityError

from django.core.exceptions import ObjectDoesNotExist


###################################################################

def crearPropietario(nomb, apell , ct , cedul , tlf1=None):
    form_data = {
            'nombres': nomb,
            'apellidos': apell,
            'cedula': cedul,
            'telefono_1' : tlf1,
            'cedulaTipo': ct
            
        }
    form = PropietarioForm(data = form_data)
    props = Propietario.objects.all()
    
    if form.is_valid():
        obj = Propietario(
                nombres = form.cleaned_data['nombres'],
                apellidos = form.cleaned_data['apellidos'],
                cedula = form.cleaned_data['cedula'],
                telefono1   = form.cleaned_data['telefono_1'],
                cedulaTipo = form.cleaned_data['cedulaTipo']

            )    
        if len(props) == 0:
             
            obj.save()
                
        
        else:    
        
            try:
                with transaction.atomic():    
                    obj.save()
            except:
                pass
        return obj
    return None

            
def crearEstacionamiento(nomb, dir , rif, propietario, tlf1=None,tlf2=None,tlf3=None,email1=None,email2=None):
    form_data = {
            'propietario': propietario.id,
            'nombre': nomb,
            'direccion': dir,
            'rif': rif,
            'telefono_1': tlf1,
            'telefono_2': tlf2,
            'telefono_3': tlf3,
            'email_1': email1,
            'email_2': email2
        }
    form = EstacionamientoForm(data = form_data)
    
    if form.is_valid():
        obj = Estacionamiento(
            nombre      = form.cleaned_data['nombre'],
            direccion   = form.cleaned_data['direccion'],
            rif         = form.cleaned_data['rif'],
            telefono1   = form.cleaned_data['telefono_1'],
            telefono2   = form.cleaned_data['telefono_2'],
            telefono3   = form.cleaned_data['telefono_3'],
            email1      = form.cleaned_data['email_1'],
            email2      = form.cleaned_data['email_2'],
            propietario = form.cleaned_data['propietario']
        )
        try:
            with transaction.atomic():    
                obj.save()
        finally:
            pass
    return obj
            

def modificarPropietario(cts,cedsearch, nomb, apell, ct, cedul, tlf1=None):
    try:
        Propietario.objects.get(cedula= cedsearch,cedulaTipo=cts)
    except:
        return False
                   
    form_data_buscar = {
            'nombres': 'asd',
            'apellidos': 'asd',
            'cedula': cedsearch,
            'telefono_1': tlf1,
            'cedulaTipo': cts
        }
    form_data_modif = {
            'nombres': nomb,
            'apellidos': apell,           
            'cedula': cedul,
            'telefono_1': tlf1,
            'cedulaTipo': ct
        }
    form1 = PropietarioForm(data = form_data_buscar)
    form2 = PropietarioForm(data = form_data_modif)
            
    if (form1.is_valid()) and (form2.is_valid()) :
        x = False
        try:
            with transaction.atomic():        
                Propietario.objects.filter(cedula= cedsearch,cedulaTipo=cts).update(
                    nombres     = form2.cleaned_data['nombres'],
                    apellidos   = form2.cleaned_data['apellidos'],
                    cedula      = form2.cleaned_data['cedula'],
                    cedulaTipo  = form2.cleaned_data['cedulaTipo'],
                    telefono1   = form2.cleaned_data['telefono_1']
                )
                x = True
        except:
            pass 
        return x
    return False

def cambiarPropietario(estacionamiento,ct,cedul):
    form_cedula = {
            'cedulaTipo': ct,
            'cedula': cedul
        }
    
    form = CedulaForm(data = form_cedula)
    x = False        
    if form.is_valid() :
        try:
            with transaction.atomic(): 
                propietario=Propietario.objects.get(cedulaTipo=ct, cedula=cedul)
                Estacionamiento.objects.filter(id = estacionamiento.id).update(
                    propietario=propietario
                    )       
            x = True
        except:
            pass
    return x

class PropietarioModTestCase(TestCase):
    
    #TDD
    def testModificarPropietario_CheckDatabase(self):
        crearPropietario('Larry Jhosue', 'Perez Gonzalez', 'V', '24042840')
        tst = modificarPropietario( 'V', '24042840', 'Larry Capinga', 'Perez Perez', 'E', '24042841','04120000000')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
    
    #Malicia
    def testModificarPropietario_NotFound(self):
        crearPropietario('Larry Jose', 'Perez Gonzales', 'V', '24042840',  '04128989898')
        tst = modificarPropietario('V','99987639', 'Larry Capinga', 'Perez Perez', 'V', '24042841','04120000000')
        self.assertFalse(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
    
    #Malicia    
    def testModificarPropietario_CedulaExistente(self):
        crearPropietario('Guigue', 'Perez', 'V', '4444',  '04128987654')
        crearPropietario('Ana', 'Bell', 'E', '5689',  '04263579468')
        self.assertEqual(len(Propietario.objects.all()), 2)
        tst = modificarPropietario('E','5689', 'Larry', 'Perez', 'V', '4444' ,'04240987654')
        self.assertFalse(tst)
        self.assertEqual(len(Propietario.objects.all()), 2)
    
    #Esquina    
    def testModificarPropietario_PorElMismo(self):
        crearPropietario('Pepe', 'Bell', 'E', '1234')
        self.assertEqual(len(Propietario.objects.all()), 1)
        tst = modificarPropietario( 'E','1234', 'Pepe',  'Bell', 'E', '1234')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
    
    #Esquina    
    def testModificarPropietario_PorEsquina(self):
        crearPropietario('Ana', 'Bell', 'V', '5689',  '04263579468')
        self.assertEqual(len(Propietario.objects.all()), 1)
        tst = modificarPropietario('V','5689', 'A', 'A', 'E', '0')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
    
    #Borde    
    def testModificarPropietario_NombreCaracteresEspeciales(self):
        crearPropietario('Ana', 'Bell','V', '5689', '04263579468')
        self.assertEqual(len(Propietario.objects.all()), 1)
        tst = modificarPropietario('V','5689', '\'-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ', 'Perez','V', '5689' ,'04240987654')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
        
    #Borde    
    def testModificarPropietario_ApellidoCaracteresEspeciales(self):
        crearPropietario('Ana', 'Bell',  'V', '5689', '04263579468')
        self.assertEqual(len(Propietario.objects.all()), 1)
        tst = modificarPropietario( 'V','5689', 'Ana', '\'-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ','V', '5689' ,'04240987654')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)

    #########################################################
    #               TESTS CAMBIAR PROPIETARIO               #
    #########################################################
    
    #TDD
    def testCambiarPropietario_CheckDatabase(self):
        propietario=crearPropietario('Larry Jhosue', 'Perez Gonzalez', 'V', '24042840')
        propietario2=crearPropietario('Pepe', 'Pepeto', 'V', '24')
        estacionamiento=crearEstacionamiento('EstacionaTech', 'Aca', 'V-123456789', propietario)
        tst = cambiarPropietario(estacionamiento,'V','24')
        self.assertTrue(tst)
        self.assertEqual(len(Estacionamiento.objects.all()), 1)
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech').propietario, propietario2)
        
    #Borde
    def testCambiarPropietario_MismoPropietario(self):
        propietario=crearPropietario('Larry Jhosue', 'Perez Gonzalez', 'V', '24042840')
        estacionamiento=crearEstacionamiento('EstacionaTech', 'Aca', 'V-123456789', propietario)
        tst = cambiarPropietario(estacionamiento,'V','24042840')
        self.assertTrue(tst)
        self.assertEqual(len(Estacionamiento.objects.all()), 1)
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech').propietario, propietario)
        
    #Esquina
    def testCambiarPropietario_DosEstacionamientosMismoDueno(self):
        propietario=crearPropietario('Larry Jhosue', 'Perez Gonzalez', 'V', '24042840')
        crearEstacionamiento('EstacionaTech', 'Aca', 'V-123456789', propietario)
        crearEstacionamiento('EstacionaTech1', 'Aca', 'V-123456789', propietario)
        tst = modificarPropietario( 'V','24042840', 'Neo', 'Neote', 'V', '123456')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
        self.assertEqual(len(Estacionamiento.objects.all()), 2)
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech').propietario.nombres
                         , 'Neo')
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech1').propietario.nombres
                         , 'Neo')
        
    #Malicia
    def testCambiarPropietario_NoExistente(self):
        propietario=crearPropietario('Larry Jhosue', 'Perez Gonzalez', 'V', '24042840')
        estacionamiento=crearEstacionamiento('EstacionaTech', 'Aca', 'V-123456789', propietario)
        tst = cambiarPropietario(estacionamiento,'V','24')
        self.assertFalse(tst)
        self.assertEqual(len(Estacionamiento.objects.all()), 1)
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech').propietario, propietario)   
    