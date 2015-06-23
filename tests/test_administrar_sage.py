from estacionamientos.models import AdministracionSage
from decimal import Decimal

import unittest


class TestAdministrarSage(unittest.TestCase):

    # interior
    def test_creacion_administrador_sage(self):
        AdministracionSage.objects.create_AdministracionSage()
        numAdministracion = len(AdministracionSage.objects.all())
        AdministracionSage.objects.all().delete()
        self.assertEqual(numAdministracion, 1)
    
    # malicia    
    def test_crear_dos_instancias(self):
        AdministracionSage.objects.create_AdministracionSage()
        AdministracionSage.objects.create_AdministracionSage()
        numAdministracion = len(AdministracionSage.objects.all())
        AdministracionSage.objects.all().delete()
        self.assertEqual(numAdministracion, 1)
        
    # interior
    def test_porcentaje_inicial_cero(self):
        AdministracionSage.objects.create_AdministracionSage()
        administracion = AdministracionSage.objects.get(pk = 1)
        AdministracionSage.objects.all().delete()
        self.assertEqual(administracion.porcentaje, 0)
    
    # borde
    def test_cambiar_porcentaje_negativo(self):
        AdministracionSage.objects.create_AdministracionSage()
        administracion = AdministracionSage.objects.get(pk = 1)
        administracion.cambiar_porcentaje(-0.1)
        AdministracionSage.objects.all().delete()
        self.assertEqual(administracion.porcentaje, 0)
        
    # borde    
    def test_cambiar_porcentaje_limite_superior(self):
        administracion = AdministracionSage()
        administracion.save()
        administracion = AdministracionSage.objects.get(pk = 1)
        administracion.cambiar_porcentaje(Decimal('9.9'))
        AdministracionSage.objects.all().delete() 
        self.assertEqual(administracion.porcentaje, Decimal('9.9'))
    
    # borde    
    def test_cambiar_porcentaje_invalido_superior(self):
        administracion = AdministracionSage()
        administracion.save()
        administracion = AdministracionSage.objects.get(pk = 1)
        administracion.cambiar_porcentaje(Decimal('10.0'))
        AdministracionSage.objects.all().delete() 
        self.assertEqual(administracion.porcentaje, 0)
        
    