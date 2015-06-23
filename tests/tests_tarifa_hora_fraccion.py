# -*- coding: utf-8 -*-

from django.test import TestCase

from datetime import datetime

from estacionamientos.models import TarifaHorayFraccion
        


###################################################################
# TARIFA HORA Y FRACCION
###################################################################

class TarifaHoraFraccionTestCase(TestCase):

            #########################
            # TDD
            #########################

    def test_tarifa_hora_y_fraccion_una_dos_horas(self):
        initial_time = datetime(2015,2,18,13,0)
        final_time = datetime(2015,2,18,15,0)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),4)

    def test_tarifa_hora_y_fraccion_media_hora(self):
        initial_time = datetime(2015,2,18,13,15)
        final_time = datetime(2015,2,18,13,45)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),2)

    def test_tarifa_hora_y_fraccion_una_hora(self):
        initial_time = datetime(2015,2,18,13,0)
        final_time = datetime(2015,2,18,14,0)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),2)
        
    def test_tarifa_hora_y_fraccion_un_dia(self): # Normal
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,0)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),48)

    def test_tarifa_hora_y_fraccion_una_hora_fraccion_15_minutos(self):
        initial_time = datetime(2015,2,18,19,0)
        final_time = datetime(2015,2,18,20,15)
        rate = TarifaHorayFraccion(tarifa = 1)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),1.5)

    def test_tarifa_hora_y_fraccion_dos_dias(self):
        initial_time = datetime(2015,2,18,6,30)
        final_time = datetime(2015,2,20,6,30)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),96)

    def test_tarifa_hora_y_fraccion_dos_dias_mas_un_minuto(self):
        initial_time = datetime(2015,2,18,6,30)
        final_time = datetime(2015,2,20,6,31)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),97)

            #########################
            # BORDES
            #########################

    #tarifa = 0
    def test_tarifa_hora_y_fraccion_dos_dias(self):
        initial_time = datetime(2015,2,18,6,30)
        final_time = datetime(2015,2,20,6,30)
        rate = TarifaHorayFraccion(tarifa_D = 0)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Discapacitado'),0)

    #una hora y media
    def test_tarifa_hora_y_fraccion_una_hora_mas_media_hora(self):
        initial_time = datetime(2015,2,18,13,0)
        final_time = datetime(2015,2,18,14,30)
        rate = TarifaHorayFraccion(tarifa = 20)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),30)

    #una hora y 31 minutos
    def test_tarifa_hora_y_fraccion_una_hora_mas_media_hora_mas_1_minuto(self):
        initial_time = datetime(2015,2,18,15,15)
        final_time = datetime(2015,2,18,16,46)
        rate = TarifaHorayFraccion(tarifa_C = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Camion'),4)

    #un dia 
    def test_tarifa_hora_y_fraccion_un_dia(self): # Borde
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,18,23,59)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),48)

    #un dia y un minuto
    def test_tarifa_hora_y_fraccion_un_dia_mas_un_minuto(self): # Borde
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,1)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),49)

    #un dia y media hora
    def test_tarifa_hora_y_fraccion_un_dia_mas_media_hora(self):
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,30)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),49)

    #un dia y 31 minutos
    def test_tarifa_hora_y_fraccion_un_dia_mas_media_hora_mas_un_minuto(self):
        initial_time = datetime(2015,2,18,0,0)
        final_time = datetime(2015,2,19,0,31)
        rate = TarifaHorayFraccion(tarifa_C = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Camion'),50)

    def test_tarifa_hora_y_fraccion_un_dia_antes_de_la_medianoche_mas_un_minuto(self):
        initial_time = datetime(2015,2,18,23,59)
        final_time = datetime(2015,2,20,0,0)
        rate = TarifaHorayFraccion(tarifa_M = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Moto'),49)

    def test_tarifa_hora_y_fraccion_un_dia_treinta_minutos_antes_de_la_medianoche_mas_treinta_minutos(self):
        initial_time = datetime(2015,2,18,23,30)
        final_time = datetime(2015,2,20,0,0)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),49)

    def test_tarifa_hora_y_fraccion_un_dia_treinta_minutes_antes_de_la_medianoche_mas_treinta_y_un_minutos(self):
        initial_time = datetime(2015,2,18,23,30)
        final_time = datetime(2015,2,20,0,1)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),50)

            #########################
            # ESQUINA
            #########################

    def test_tarifa_hora_y_fraccion_quince_dias(self): # Esquina
        initial_time = datetime(2015,2,10,6,30)
        final_time = datetime(2015,2,25,6,30)
        rate = TarifaHorayFraccion(tarifa = 2)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),15*24*2)

    def test_tarifa_hora_y_fraccion_una_hora_mas_media_hora_tarifa_cero(self):
        initial_time = datetime(2015,2,18,13,0)
        final_time = datetime(2015,2,18,14,30)
        rate = TarifaHorayFraccion(tarifa = 0)
        self.assertEqual(rate.calcularPrecio(initial_time,final_time,'Particular'),0)
