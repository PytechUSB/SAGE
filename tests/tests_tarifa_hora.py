# -*- coding: utf-8 -*-

from django.test import TestCase

from datetime import datetime

from estacionamientos.models import TarifaHora
        


###################################################################
# Casos de prueba de tipos de tarifa
###################################################################

class TarifaHoraTestCase(TestCase):

    ###################################################################
    # PARTICULARES
    ###################################################################

            #########################
            # TDD
            #########################

    def test_tarifa_hora_una_hora(self): # TDD
        rate = TarifaHora(tarifa = 800)
        initial_datetime = datetime(2015,2,18,13,0)
        final_datetime = datetime(2015,2,18,14,0)
        value = rate.calcularPrecio(initial_datetime, final_datetime,'Particular')
        self.assertEquals(value, 800)

    def test_tarifa_hora_mas_de_una_hora(self): # TDD
        rate = TarifaHora(tarifa = 800)
        initial_datetime = datetime(2015,2,18,6,8)
        final_datetime = datetime(2015,2,18,7,9)
        value = rate.calcularPrecio(initial_datetime, final_datetime,'Particular')
        self.assertEquals(value, 1600)

            #########################
            # BORDE
            #########################

    def test_tarifa_hora_menos_de_una_hora(self): 
        rate = TarifaHora(tarifa = 800)
        initial_datetime = datetime(2015,2,18,11,0)
        final_datetime = datetime(2015,2,18,11,15)
        value = rate.calcularPrecio(initial_datetime, final_datetime,'Particular')
        self.assertEquals(value, 800)

    def test_tarifa_hora_dia_completo_menos_un_minuto(self): 
        rate=TarifaHora(tarifa=1)
        initial_time=datetime(2015,2,18,0,0)
        final_time=datetime(2015,2,18,23,59)
        value = rate.calcularPrecio(initial_time, final_time,'Particular')
        self.assertEqual(value, 24)

    def test_tarifa_hora_dia_completo(self): 
        rate=TarifaHora(tarifa=1)
        initial_time=datetime(2015,2,18,0,0)
        final_time=datetime(2015,2,19,0,0)
        value = rate.calcularPrecio(initial_time, final_time,'Particular')
        self.assertEqual(value, 24)

    def test_dia_completo_mas_un_minuto(self):
        rate=TarifaHora(tarifa=1)
        initial_time=datetime(2015,2,18,0,0)
        final_time=datetime(2015,2,19,0,1)
        value = rate.calcularPrecio(initial_time, final_time,'Particular')
        self.assertEqual(value, 25)

    def test_tarifa_hora_quince_dias(self):
        rate=TarifaHora(tarifa=1)
        initial_time=datetime(2015,2,10,0,0)
        final_time=datetime(2015,2,25,0,0)
        value = rate.calcularPrecio(initial_time, final_time,'Particular')
        self.assertEqual(value, 24*15)

    ###################################################################
    # MOTOS
    ###################################################################

    #tarifa = 0
    def test_tarifa_hora_tarifa_cero_M(self): 
        rate=TarifaHora(tarifa_M=0)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,9,30)
        value = rate.calcularPrecio(initial_time, final_time,'Moto')
        self.assertEqual(value, 0)

    #una hora
    def test_tarifa_hora_una_hora_M(self): 
        rate=TarifaHora(tarifa_M=60)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,4,0)
        value = rate.calcularPrecio(initial_time, final_time,'Moto')
        self.assertEqual(value, 60)

    #un hora y un minuto
    def test_tarifa_hora_una_hora_un_minuto_M(self): 
        rate=TarifaHora(tarifa_M=60)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,4,1)
        value = rate.calcularPrecio(initial_time, final_time,'Moto')
        self.assertEqual(value, 120)

    ###################################################################
    # CAMIONES
    ###################################################################

    #tarifa = 0
    def test_tarifa_hora_tarifa_cero_C(self): 
        rate=TarifaHora(tarifa_C=0)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,9,30)
        value = rate.calcularPrecio(initial_time, final_time,'Camion')
        self.assertEqual(value, 0)

    #una hora
    def test_tarifa_hora_una_hora_C(self): 
        rate=TarifaHora(tarifa_C=60)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,4,0)
        value = rate.calcularPrecio(initial_time, final_time,'Camion')
        self.assertEqual(value, 60)

    #un hora y un minuto
    def test_tarifa_hora_una_hora_un_minuto_C(self): 
        rate=TarifaHora(tarifa_C=60)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,4,1)
        value = rate.calcularPrecio(initial_time, final_time,'Camion')
        self.assertEqual(value, 120)

    ###################################################################
    # DISCAPACITADO
    ###################################################################

    #tarifa = 0
    def test_tarifa_hora_tarifa_cero_D(self): 
        rate=TarifaHora(tarifa_D=0)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,9,30)
        value = rate.calcularPrecio(initial_time, final_time,'Discapacitado')
        self.assertEqual(value, 0)

    #una hora
    def test_tarifa_hora_una_hora_D(self): 
        rate=TarifaHora(tarifa_D=60)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,4,0)
        value = rate.calcularPrecio(initial_time, final_time,'Discapacitado')
        self.assertEqual(value, 60)

    #un hora y un minuto
    def test_tarifa_hora_una_hora_un_minuto_D(self): 
        rate=TarifaHora(tarifa_D=60)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,4,1)
        value = rate.calcularPrecio(initial_time, final_time,'Discapacitado')
        self.assertEqual(value, 120)

    ###################################################################
    # CASOS ESQUINAS
    ###################################################################

    #una hora y traifa = 0
    def test_tarifa_hora_una_hora_tarifa_cero_D(self): 
        rate=TarifaHora(tarifa_D=0)
        initial_time=datetime(2015,2,18,3,0)
        final_time=datetime(2015,2,18,4,0)
        value = rate.calcularPrecio(initial_time, final_time,'Discapacitado')
        self.assertEqual(value, 0)

    #quince dias, tarifa=0
    def test_tarifa_hora_quince_dias_tarifa_cero(self):
        rate=TarifaHora(tarifa=0)
        initial_time=datetime(2015,2,10,0,0)
        final_time=datetime(2015,2,25,0,0)
        value = rate.calcularPrecio(initial_time, final_time,'Particular')
        self.assertEqual(value, 0)