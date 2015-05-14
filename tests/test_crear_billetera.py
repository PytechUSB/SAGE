from django.test import TestCase

from estacionamientos.models import BilleteraElectronica

from estacionamientos.forms import BilleteraForm

from django.db import transaction

from django.db.utils import IntegrityError

def crearBilletera(cedul):
    form_data = {
        'nombre': 'Carlos',
        'apellido': 'Perez',
        'cedula': cedul,
        'PIN': '1234',
        'identificador': '1000100010001000'
    }
    form = BilleteraForm(data = form_data)
    billetera = BilleteraElectronica.objects.all()
    
    if form.is_valid():
        inicial = 1000100010001000
        
        if len(billetera) == 0:
            obj = BilleteraElectronica(
                nombre = form.cleaned_data['nombre'],
                apellido = form.cleaned_data['apellido'],
                PIN = form.cleaned_data['PIN'],
                cedula = form.cleaned_data['cedula'],
                identificador = str(inicial)
                )    
            obj.save()
                
        #elif not BilleteraElectronica.objects.filter(cedula=form.cleaned_data['cedula']).exists():
        else:    
            siguiente_numero = inicial + len(billetera)
            obj = BilleteraElectronica(
                    nombre = form.cleaned_data['nombre'],
                    apellido = form.cleaned_data['apellido'],
                    PIN = form.cleaned_data['PIN'],
                    cedula = form.cleaned_data['cedula'],
                    identificador = str(siguiente_numero)
                )
            
            try:
                with transaction.atomic():    
                    obj.save()
            except (IntegrityError):
                pass 

class CrearBilleteraTestCase(TestCase):
    
        
    # borde
    def testCrearBilletera_IdentificadorInicialCorrecto(self):
        crearBilletera(str(0))
        billetera = BilleteraElectronica.objects.get(pk = 1)
        self.assertEqual(billetera.identificador, '1000100010001000')
    
    # malicia    
    def testCrearBilletera_CedulaExistente(self):
        crearBilletera(str(0))
        crearBilletera(str(0))
        self.assertEqual(len(BilleteraElectronica.objects.all()), 1)
        
