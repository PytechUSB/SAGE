from django.test import TestCase

from estacionamientos.models import BilleteraElectronica

from estacionamientos.forms import BilleteraForm

from django.db import transaction

from django.db.utils import IntegrityError

from decimal import Decimal

def crearBilletera(cedul, cedulaTipo):
    form_data = {
        'nombre': 'Carlos',
        'apellido': 'Perez',
        'cedula': cedul,
        'PIN': '1234',
        'cedulaTipo': cedulaTipo
    }
    form = BilleteraForm(data = form_data)
    billetera = BilleteraElectronica.objects.all()
    
    if form.is_valid():
        if len(billetera) == 9999:
            pass
                
        #elif not BilleteraElectronica.objects.filter(cedula=form.cleaned_data['cedula']).exists():
        else:    
            obj = BilleteraElectronica(
                    nombre = form.cleaned_data['nombre'],
                    apellido = form.cleaned_data['apellido'],
                    PIN = form.cleaned_data['PIN'],
                    cedula = form.cleaned_data['cedula'],
                    saldo = 0.00,
                    cedulaTipo = form.cleaned_data['cedulaTipo']
                )
            
            try:
                with transaction.atomic():
                    obj.save()
            except (IntegrityError):
                pass 

class CrearBilleteraTestCase(TestCase):
    
        
    # borde
    def testCrearBilletera_IdentificadorInicialCorrecto(self):
        crearBilletera(str(0), 'V')
        billetera = BilleteraElectronica.objects.get(pk = 1)
        self.assertEqual(billetera.id, 1)
    
    # malicia    
    def testCrearBilletera_CedulaExistente(self):
        crearBilletera(str(0), 'V')
        crearBilletera(str(0), 'V')
        self.assertEqual(len(BilleteraElectronica.objects.all()), 1)
        
