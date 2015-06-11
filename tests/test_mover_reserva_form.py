# -*- coding: utf-8 -*-

from django.test import TestCase
from estacionamientos.forms import MoverReservaForm
from datetime import datetime

class MoverReservaFormTestCase(TestCase):
    
    # interno
    def testMoverReserva_FormValido(self):
        form_data = {'inicio_1': datetime.now().time(),
                     'inicio_0': datetime.now().date()
                    }
        form = MoverReservaForm(data = form_data)
        self.assertTrue(form.is_valid())
    
    # borde   
    def testMoverReserva_UnCampo(self):
        form_data = {'inicio_1': datetime.now().time()
                    }
        form = MoverReservaForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def testMoverReserva_Letras(self):
        form_data = {'inicio_1': 'crty',
                     'inicio_0': datetime.now().date()
                    }
        form = MoverReservaForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def testMoverReserva_Numeros(self):
        form_data = {'inicio_1': datetime.now().time(),
                     'inicio_0': 12345
                    }
        form = MoverReservaForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def testMoverReserva_Simbolos(self):
        form_data = {'inicio_1': datetime.now().time(),
                     'inicio_0': '%&$'
                    }
        form = MoverReservaForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    # malicia
    def testMoverReserva_CamposInvertidos(self):
        form_data = {'inicio_1': datetime.now().date(),
                     'inicio_0': datetime.now().time()
                    }
        form = MoverReservaForm(data = form_data)
        self.assertFalse(form.is_valid())