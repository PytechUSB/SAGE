# -*- coding: utf-8 -*-

from django.test import TestCase

from datetime import datetime

from estacionamientos.models import TarifaMinuto
        


###################################################################
# TARIFA POR MINUTO
###################################################################

class TarifaMinutoTestCase(TestCase):

    ###################################################################
    # PARTICULARES
    ###################################################################

            #########################
            # TDD
            #########################

    def test_tarifa_minuto_dos_minutos(self): 
        initial_time = datetime(2015,2,18,15,1)
        final_time = datetime(2015,2,18,15,3)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),2)


    def test_tarifa_minuto_un_dia_mas_un_minuto(self): 
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,1)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),1441)

            #########################
            # BORDES
            #########################

    def test_tarifa_minuto_un_minuto(self): 
        initial_time = datetime(2015,2,18,15,1)
        final_time = datetime(2015,2,18,15,2)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),1)

    def test_tarifa_minuto_una_hora(self): 
        initial_time = datetime(2015,2,18,15,0)
        final_time = datetime(2015,2,18,16,0)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),60)

    def test_tarifa_minuto_un_dia_menos_un_minuto(self): 
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,18,23,59)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),1439)

    def test_tarifa_minuto_un_dia(self): 
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,0)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),1440)

    def test_tarifa_minuto_un_dia_antes_de_la_medianoche_mas_un_minuto(self): 
        initial_time = datetime(2015,2,18,23,59)
        final_time = datetime(2015,2,20,0,0)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),1441)

    #tarifa con valor cero
    def test_tarifa_minuto_valor_cero(self): 
        initial_time = datetime(2015,2,18,20,0)
        final_time = datetime(2015,2,18,22,30)
        rate = TarifaMinuto(tarifa = 0)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),0)

    #el horizonte se amplio a 15 dias
    def test_tarifa_minuto_quince_dias(self): 
        initial_time = datetime(2015,2,10,23,59)
        final_time = datetime(2015,2,25,23,59)
        rate = TarifaMinuto(tarifa = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),15*24*60)

            #########################
            # ESQUINA
            #########################

    #monto por 15 dias con tarifa igual a 0
    def test_tarifa_minuto_quince_dias_valor_cero(self): 
        initial_time = datetime(2015,2,18,23,59)
        final_time = datetime(2015,2,25,23,59)
        rate = TarifaMinuto(tarifa = 0)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),0)

    ###################################################################
    # MOTOS
    ###################################################################

            #########################
            # BORDES
            #########################

    def test_tarifa_minuto_un_minuto_M(self): 
        initial_time = datetime(2015,2,18,15,1)
        final_time = datetime(2015,2,18,15,2)
        rate = TarifaMinuto(tarifa_M = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Moto'),1)

    def test_tarifa_minuto_una_hora_M(self): 
        initial_time = datetime(2015,2,18,15,0)
        final_time = datetime(2015,2,18,16,0)
        rate = TarifaMinuto(tarifa_M = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Moto'),60)

    def test_tarifa_minuto_un_dia_M(self): 
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,0)
        rate = TarifaMinuto(tarifa_M = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Moto'),1440)

    #tarifa con valor cero
    def test_tarifa_minuto_valor_cero_M(self): 
        initial_time = datetime(2015,2,18,20)
        final_time = datetime(2015,2,18,22,30)
        rate = TarifaMinuto(tarifa_M = 0)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Moto'),0)

    ###################################################################
    # CAMIONES
    ###################################################################

            #########################
            # BORDES
            #########################

    def test_tarifa_minuto_un_minuto_C(self): 
        initial_time = datetime(2015,2,18,15,1)
        final_time = datetime(2015,2,18,15,2)
        rate = TarifaMinuto(tarifa_C = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Camion'),1)

    def test_tarifa_minuto_una_hora_C(self): 
        initial_time = datetime(2015,2,18,15,0)
        final_time = datetime(2015,2,18,16,0)
        rate = TarifaMinuto(tarifa_C = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Camion'),60)

    def test_tarifa_minuto_un_dia_C(self): 
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,0)
        rate = TarifaMinuto(tarifa_C = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Camion'),1440)

    #tarifa con valor cero
    def test_tarifa_minuto_valor_cero_C(self): 
        initial_time = datetime(2015,2,18,20,0)
        final_time = datetime(2015,2,18,22,30)
        rate = TarifaMinuto(tarifa_C = 0)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Camion'),0)

    ###################################################################
    # DISCAPACITADOS
    ###################################################################

            #########################
            # BORDES
            #########################

    def test_tarifa_minuto_un_minuto_D(self): 
        initial_time = datetime(2015,2,18,15,1)
        final_time = datetime(2015,2,18,15,2)
        rate = TarifaMinuto(tarifa_D = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Discapacitado'),1)

    def test_tarifa_minuto_una_hora_D(self): 
        initial_time = datetime(2015,2,18,15,0)
        final_time = datetime(2015,2,18,16,0)
        rate = TarifaMinuto(tarifa_D = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Discapacitado'),60)

    def test_tarifa_minuto_un_dia_D(self): 
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,0)
        rate = TarifaMinuto(tarifa_D = 60)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Discapacitado'),1440)

    #tarifa con valor cero
    def test_tarifa_minuto_valor_cero_D(self): 
        initial_time = datetime(2015,2,18,20,0)
        final_time = datetime(2015,2,18,22,30)
        rate = TarifaMinuto(tarifa_D = 0)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Discapacitado'),0)