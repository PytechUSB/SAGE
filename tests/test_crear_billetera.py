from django.test import TestCase

from estacionamientos.models import BilleteraElectronica

from estacionamientos.forms import BilleteraForm

from django.db import transaction

from django.db.utils import IntegrityError

from decimal import Decimal

from estacionamientos.controller import billetera_autenticar

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
    
    # interior
    def testConsultaSaldo(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        saldo = 5,
                        PIN = "1234"
        )
        billetera.save()
        billeteraE = BilleteraElectronica.objects.get(pk = 1)
        self.assertEqual(billeteraE.saldo, 5)
    
    # malicia    
    def testConsultaSaldoNulo(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.save()
        billeteraE = BilleteraElectronica.objects.get(pk = 1)
        self.assertEqual(billeteraE.saldo, 0)
    
    # interior    
    def testCrearBilletera_AutenticarBilletera(self):
        billetera1 = BilleteraElectronica(cedula = '10', 
                                          cedulaTipo = 'V', 
                                          nombre = 'Maria', 
                                          apellido = 'Perez', 
                                          saldo = 0.00, 
                                          PIN = '1234')
        billetera1.save()
        billetera = billetera_autenticar(1, "1234")
        self.assertEqual(billetera1, billetera)
        
    # malicia
    def testCrearBilletera_AutenticarPINinvalido(self):
        billetera = BilleteraElectronica(cedula = '11', 
                                         cedulaTipo = 'V', 
                                         nombre = 'Mario', 
                                         apellido = 'Jimenez', 
                                         saldo = 0.00, 
                                         PIN = '1234')
        billetera.save()
        billetera1 = billetera_autenticar(1, '1235')
        self.assertNotEqual(billetera, billetera1)
       
    # borde    
    def testCrearBilletera_AutenticarIDinvalido(self):
        billetera = BilleteraElectronica(cedula = '10', 
                                         cedulaTipo = 'V', 
                                         nombre = 'Maria', 
                                         apellido = 'Perez', 
                                         saldo = 0.00, 
                                         PIN = '1234')
        billetera.save()
        billetera1 = billetera_autenticar(2, '1234')
        self.assertNotEqual(billetera, billetera1)
        
    # borde    
    def testCrearBilletera_AutenticarInvalido(self):
        billetera = BilleteraElectronica(cedula = '10', 
                                         cedulaTipo = 'V', 
                                         nombre = 'Maria', 
                                         apellido = 'Perez', 
                                         saldo = 0.00, 
                                         PIN = '1234')
        billetera.save()
        billetera1 = billetera_autenticar(2, '1235')
        self.assertNotEqual(billetera, billetera1)
        
    # malicia
    def testCrearBilletera_AutenticarNull(self):
        billetera = billetera_autenticar(10, '1234')
        self.assertEqual(billetera, None)
    
    # borde    
    def testValidarRecargaCero(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        self.assertFalse(billetera.validar_recarga(0))
        
    # borde    
    def testValidarRecargaLimiteInferior(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        self.assertTrue(billetera.validar_recarga(Decimal(0.01)))
    
    # borde    
    def testValidarRecargaLimiteSuperior(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        self.assertTrue(billetera.validar_recarga(Decimal(10000.00)))
    
    # borde    
    def testValidarRecargaInvalida(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        self.assertFalse(billetera.validar_recarga(Decimal(10000.001)))
        
    # malicia
    def testValidarRecargaNegativa(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        self.assertFalse(billetera.validar_recarga(Decimal(-0.01)))
        
    # malicia
    def testValidarRecargaCaracterEspecial(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        self.assertFalse(billetera.validar_recarga("@"))
        
    # malicia
    def testValidarRecargaNumeroString(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        self.assertFalse(billetera.validar_recarga("1"))
    
    # borde    
    def testValidarConsumoNegativo(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        self.assertFalse(billetera.validar_consumo(-0.01))
        
    # borde    
    def testValidarConsumoLimiteInferior(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        self.assertTrue(billetera.validar_consumo(0))
    
    # borde    
    def testValidarConsumoLimiteSuperior(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        saldo = Decimal(10000.00),
                        PIN = "1234"
        )
        self.assertTrue(billetera.validar_consumo(10000.00))
    
    # borde    
    def testValidarConsumoInvalido(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        saldo = Decimal(10000.00),
                        PIN = "1234"
        )
        self.assertFalse(billetera.validar_consumo(Decimal(10000.001)))
    
    # malicia    
    def testValidarConsumoMontoString(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        saldo = Decimal(10000.00),
                        PIN = "1234"
        )
        self.assertFalse(billetera.validar_consumo("1"))
        
    # malicia
    def testValidarConsumoMontoCaracterEspecial(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        saldo = Decimal(10000.00),
                        PIN = "1234"
        )
        self.assertFalse(billetera.validar_consumo("%"))
    
    # borde    
    def testRecargarSaldoCero(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(0)
        self.assertEqual(billetera.saldo, 0)
        
    # borde    
    def testRecargarSaldoNegativo(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(Decimal(-0.01))
        self.assertEqual(billetera.saldo, 0)
        
    # borde    
    def testRecargarSaldoLimiteInferior(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(Decimal(0.01))
        self.assertEqual(billetera.saldo, Decimal('0.01'))
        
    # borde    
    def testRecargarSaldoLimiteSuperior(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(10000)
        self.assertEqual(billetera.saldo, 10000)
        
    # borde    
    def testRecargarSaldoInvalido(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(Decimal(10000.01))
        self.assertEqual(billetera.saldo, 0)
        
    # malicia    
    def testRecargarSaldoMontoString(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo("1")
        self.assertEqual(billetera.saldo, 0)
        
    # malicia    
    def testRecargarSaldoCaracterEspecial(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo("&")
        self.assertEqual(billetera.saldo, 0)
        
    # borde
    def testConsumirSaldoCero(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(10)
        billetera.consumir_saldo(0)
        self.assertEqual(billetera.saldo, 10)
        
    # borde
    def testConsumirSaldoNegativo(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(10)
        billetera.consumir_saldo(Decimal('-0.01'))
        self.assertEqual(billetera.saldo, 10)
        
    # borde
    def testConsumirSaldoLimiteInferior(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(10)
        billetera.consumir_saldo(Decimal('0.01'))
        self.assertEqual(billetera.saldo, Decimal('9.99'))
        
    # borde
    def testConsumirSaldoLimiteSuperior(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(10000)
        billetera.consumir_saldo(10000)
        self.assertEqual(billetera.saldo, 0)
        
    # borde
    def testConsumirSaldoInvalido(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(10000)
        billetera.consumir_saldo(10000.01)
        self.assertEqual(billetera.saldo, 10000)
        
    # malicia
    def testConsumirSaldoMontoString(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        billetera.recargar_saldo(10)
        billetera.consumir_saldo("1")
        self.assertEqual(billetera.saldo, 10)
        
    # malicia
    def testConsumirSaldoCaracterEspecial(self):
        billetera = BilleteraElectronica(
                        nombre = 'Alejandro',
                        apellido = 'Banega',
                        cedula = "12345678",
                        cedulaTipo = 'V',
                        PIN = "1234"
        )
        
        billetera.recargar_saldo(10)
        billetera.consumir_saldo("$")
        self.assertEqual(billetera.saldo, 10)
        
        
    
    
    
