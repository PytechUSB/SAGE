# -*- coding: utf-8 -*-

from django.test import TestCase

from estacionamientos.forms import PropietarioForm

from estacionamientos.models import Propietario

from django.db import transaction

from django.db.utils import IntegrityError


###################################################################
#                    PROPIETARIO_ALL FORM
###################################################################

def crearPropietario(nomb, apell , cedul):
    form_data = {
            'nombres': nomb,
            'apellidos': apell,
            'cedula': cedul
        }
    form = PropietarioForm(data = form_data)
    props = Propietario.objects.all()
    
    if form.is_valid():
                
        if len(props) == 0:
            obj = Propietario(
                nombres = form.cleaned_data['nombres'],
                apellidos = form.cleaned_data['apellidos'],
                cedula = form.cleaned_data['cedula']
                )    
            obj.save()
                
        #elif not PropietarioForm.objects.filter(cedula=form.cleaned_data['cedula']).exists():
        else:    
            obj = Propietario(
                nombres = form.cleaned_data['nombres'],
                apellidos = form.cleaned_data['apellidos'],
                cedula = form.cleaned_data['cedula']

                ) 
            try:
                with transaction.atomic():    
                    obj.save()
            except (IntegrityError):
                pass 
            
            
            

def modificarPropietario(cedsearch, nomb, apell, cedul):
    form_data_buscar = {
            'nombres': 'asd',
            'apellidos': 'asd',
            'cedula': cedsearch
        }
    form_data_modif = {
            'nombres': nomb,
            'apellidos': apell,
            'cedula': cedul
        }
    form1 = PropietarioForm(data = form_data_buscar)
    form2 = PropietarioForm(data = form_data_modif)
    props = Propietario.objects.all()
    
    if (form1.is_valid()) and (form2.is_valid()) :
        for obj in props:        
            if obj.cedula== cedsearch:
                obj.cedula = cedul
                obj.nombres= nomb
                obj.apellidos = apell
                return True
        return False
    print('Invalid  form')
    return False


class PropietarioModTestCase(TestCase):
    
    def testModificarPropietario_CheckDatabase(self):
        crearPropietario('Larry Jhosue', 'Perez Gonzalez', '24042840')
        tst = modificarPropietario('24042840', 'Larry Capinga', 'Perez Perez', '24042841')
        self.assertTrue(tst)
    
    def testModificarPropietario_NotFound(self):
        crearPropietario('Larry Jose', 'Perez Gonzales', '24042840')
        tst = modificarPropietario('99987639', 'Larry Capinga', 'Perez Perez', '24042841')
        self.assertFalse(tst)
     
