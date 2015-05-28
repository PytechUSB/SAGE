# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import PropietarioForm,EstacionamientoForm,CedulaForm

from estacionamientos.models import Propietario,Estacionamiento

from django.db import transaction

from django.db.utils import IntegrityError


###################################################################

def crearPropietario(nomb, apell , cedul , tlf1=None):
    form_data = {
            'nombres': nomb,
            'apellidos': apell,
            'cedula': cedul,
            'telefono_1' : tlf1
            
        }
    form = PropietarioForm(data = form_data)
    props = Propietario.objects.all()
    
    if form.is_valid():
          
        if len(props) == 0:
            obj = Propietario(
                nombres = form.cleaned_data['nombres'],
                apellidos = form.cleaned_data['apellidos'],
                cedula = form.cleaned_data['cedula'],
                telefono1   = form.cleaned_data['telefono_1']

                )    
            obj.save()
                
        #elif not PropietarioForm.objects.filter(cedula=form.cleaned_data['cedula']).exists():
        else:    
            obj = Propietario(
                nombres = form.cleaned_data['nombres'],
                apellidos = form.cleaned_data['apellidos'],
                cedula = form.cleaned_data['cedula'],
                telefono1   = form.cleaned_data['telefono_1']

                ) 
            try:
                with transaction.atomic():    
                    obj.save()
            except:
                pass
    return obj
            
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
            

def modificarPropietario(cedsearch, nomb, apell, cedul, tlf1=None):
    form_data_buscar = {
            'nombres': 'asd',
            'apellidos': 'asd',
            'cedula': cedsearch,
            'telefono_1': tlf1
        }
    form_data_modif = {
            'nombres': nomb,
            'apellidos': apell,
            'cedula': cedul,
            'telefono_1': tlf1
        }
    form1 = PropietarioForm(data = form_data_buscar)
    form2 = PropietarioForm(data = form_data_modif)
    props = Propietario.objects.all()
            
    if (form1.is_valid()) and (form2.is_valid()) :
        x = False
        for obj in props:        
            if obj.cedula==cedsearch:
                try:
                    with transaction.atomic():        
                        Propietario.objects.filter(cedula= cedsearch).update(
                            nombres     = form2.cleaned_data['nombres'],
                            apellidos   = form2.cleaned_data['apellidos'],
                            cedula      = form2.cleaned_data['cedula'],
                            telefono1   = form2.cleaned_data['telefono_1']
                        )
                        x = True
                except:
                    pass 
                finally:
                    break
        return x
    return False

def cambiarPropietario(estacionamiento,cedula):
    form_cedula = {
            'cedula': cedula
        }
    
    form = CedulaForm(data = form_cedula)
    x = False        
    if form.is_valid() :
        try:
            with transaction.atomic(): 
                propietario=Propietario.objects.get(cedula=cedula)
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
        crearPropietario('Larry Jhosue', 'Perez Gonzalez', '24042840')
        tst = modificarPropietario('24042840', 'Larry Capinga', 'Perez Perez', '24042841','04120000000')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
    
    #Malicia
    def testModificarPropietario_NotFound(self):
        crearPropietario('Larry Jose', 'Perez Gonzales', '24042840','04128989898')
        tst = modificarPropietario('99987639', 'Larry Capinga', 'Perez Perez', '24042841','04120000000')
        self.assertFalse(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
    
    #Malicia    
    def testModificarPropietario_CedulaExistente(self):
        crearPropietario('Guigue', 'Perez', '4444', '04128987654')
        crearPropietario('Ana', 'Bell', '5689', '04263579468')
        self.assertEqual(len(Propietario.objects.all()), 2)
        tst = modificarPropietario('5689', 'Larry', 'Perez', '4444' ,'04240987654')
        self.assertFalse(tst)
        self.assertEqual(len(Propietario.objects.all()), 2)
    
    #Esquina    
    def testModificarPropietario_PorElMismo(self):
        crearPropietario('Pepe', 'Bell', '1234')
        self.assertEqual(len(Propietario.objects.all()), 1)
        tst = modificarPropietario('1234', 'Pepe', 'Bell', '1234')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
    
    #Esquina    
    def testModificarPropietario_PorEsquina(self):
        crearPropietario('Ana', 'Bell', '5689', '04263579468')
        self.assertEqual(len(Propietario.objects.all()), 1)
        tst = modificarPropietario('5689', 'A', 'A', '0')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
    
    #Borde    
    def testModificarPropietario_NombreCaracteresEspeciales(self):
        crearPropietario('Ana', 'Bell', '5689', '04263579468')
        self.assertEqual(len(Propietario.objects.all()), 1)
        tst = modificarPropietario('5689', '\'-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ', 'Perez', '5689' ,'04240987654')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
        
    #Borde    
    def testModificarPropietario_ApellidoCaracteresEspeciales(self):
        crearPropietario('Ana', 'Bell', '5689', '04263579468')
        self.assertEqual(len(Propietario.objects.all()), 1)
        tst = modificarPropietario('5689', 'Ana', '\'-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ', '5689' ,'04240987654')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)

    #########################################################
    #               TESTS CAMBIAR PROPIETARIO               #
    #########################################################
    
    #TDD
    def testCambiarPropietario_CheckDatabase(self):
        propietario=crearPropietario('Larry Jhosue', 'Perez Gonzalez', '24042840')
        propietario2=crearPropietario('Pepe', 'Pepeto', '24')
        estacionamiento=crearEstacionamiento('EstacionaTech', 'Aca', 'V-123456789', propietario)
        tst = cambiarPropietario(estacionamiento,'24')
        self.assertTrue(tst)
        self.assertEqual(len(Estacionamiento.objects.all()), 1)
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech').propietario, propietario2)
        
    #Borde
    def testCambiarPropietario_MismoPropietario(self):
        propietario=crearPropietario('Larry Jhosue', 'Perez Gonzalez', '24042840')
        estacionamiento=crearEstacionamiento('EstacionaTech', 'Aca', 'V-123456789', propietario)
        tst = cambiarPropietario(estacionamiento,'24042840')
        self.assertTrue(tst)
        self.assertEqual(len(Estacionamiento.objects.all()), 1)
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech').propietario, propietario)
        
    #Esquina
    def testCambiarPropietario_DosEstacionamientosMismoDueno(self):
        propietario=crearPropietario('Larry Jhosue', 'Perez Gonzalez', '24042840')
        crearEstacionamiento('EstacionaTech', 'Aca', 'V-123456789', propietario)
        crearEstacionamiento('EstacionaTech1', 'Aca', 'V-123456789', propietario)
        tst = modificarPropietario('24042840', 'Neo', 'Neote', '123456')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
        self.assertEqual(len(Estacionamiento.objects.all()), 2)
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech').propietario.nombres
                         , 'Neo')
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech1').propietario.nombres
                         , 'Neo')
        
    #Malicia
    def testCambiarPropietario_NoExistente(self):
        propietario=crearPropietario('Larry Jhosue', 'Perez Gonzalez', '24042840')
        estacionamiento=crearEstacionamiento('EstacionaTech', 'Aca', 'V-123456789', propietario)
        tst = cambiarPropietario(estacionamiento,'24')
        self.assertFalse(tst)
        self.assertEqual(len(Estacionamiento.objects.all()), 1)
        self.assertEqual(Estacionamiento.objects.get(nombre='EstacionaTech').propietario, propietario)   
    