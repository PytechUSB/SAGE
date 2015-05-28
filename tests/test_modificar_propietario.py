# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import PropietarioForm

from estacionamientos.models import Propietario

from django.db import transaction

from django.db.utils import IntegrityError


###################################################################

def crearPropietario(nomb, apell , cedul , tlf1):
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
                telefono_1   = form.cleaned_data['telefono_1']

                )    
            obj.save()
                
        #elif not PropietarioForm.objects.filter(cedula=form.cleaned_data['cedula']).exists():
        else:    
            obj = Propietario(
                nombres = form.cleaned_data['nombres'],
                apellidos = form.cleaned_data['apellidos'],
                cedula = form.cleaned_data['cedula'],
                telefono_1   = form.cleaned_data['telefono_1']

                ) 
            try:
                with transaction.atomic():    
                    obj.save()
            except (IntegrityError):
                pass 
            
            
            

def modificarPropietario(cedsearch, nomb, apell, cedul, tlf1):
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
                            telefono_1   = form2.cleaned_data['telefono_1']
                        )
                        x = True
                except (IntegrityError):
                    pass 
                finally:
                    break
        return x
    print('Invalid  form')
    return False


class PropietarioModTestCase(TestCase):
    
    def testModificarPropietario_CheckDatabase(self):
        crearPropietario('Larry Jhosue', 'Perez Gonzalez', '24042840','04120000000')
        tst = modificarPropietario('24042840', 'Larry Capinga', 'Perez Perez', '24042841','04120000000')
        self.assertTrue(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
    
    def testModificarPropietario_NotFound(self):
        crearPropietario('Larry Jose', 'Perez Gonzales', '24042840','04128989898')
        tst = modificarPropietario('99987639', 'Larry Capinga', 'Perez Perez', '24042841','04120000000')
        self.assertFalse(tst)
        self.assertEqual(len(Propietario.objects.all()), 1)
        
    def testModificarPropietario_CedulaExistente(self):
        crearPropietario('Guigue', 'Perez', '4444', '04128987654')
        crearPropietario('Ana', 'Bell', '5689', '04263579468')
        self.assertEqual(len(Propietario.objects.all()), 2)
        tst = modificarPropietario('5689', 'Larry', 'Perez', '4444' ,'04240987654')
        self.assertFalse(tst)
        self.assertEqual(len(Propietario.objects.all()), 2)
        
