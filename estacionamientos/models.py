# -*- coding: utf-8 -*-
from django.db import models
from math import ceil, floor
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal, ROUND_DOWN
from datetime import timedelta, datetime
SMAX = 10000

class Propietario(models.Model):
	nombres     = models.CharField(max_length = 30)
	apellidos   = models.CharField(max_length = 30)
	cedula      = models.CharField(max_length = 12, unique=True)
	telefono1   = models.CharField(blank = True, null = True, max_length = 30)

	def __str__(self):
		return self.nombres+' '+self.apellidos

class Estacionamiento(models.Model):
	nombre      = models.CharField(max_length = 50)
	direccion   = models.TextField(max_length = 120)
	rif         = models.CharField(max_length = 12)
	telefono1   = models.CharField(blank = True, null = True, max_length = 30)
	telefono2   = models.CharField(blank = True, null = True, max_length = 30)
	telefono3   = models.CharField(blank = True, null = True, max_length = 30)
	email1      = models.EmailField(blank = True, null = True)
	email2      = models.EmailField(blank = True, null = True)
	
	# Campo que referencia al propietario del estacionamiento
	propietario = models.ForeignKey(Propietario)

	# Campos para referenciar al esquema de tarifa
	content_type = models.ForeignKey(ContentType, null = True)
	object_id    = models.PositiveIntegerField(null = True)
	tarifa       = GenericForeignKey()
	apertura     = models.TimeField(blank = True, null = True)
	cierre       = models.TimeField(blank = True, null = True)
	capacidad    = models.IntegerField(blank = True, null = True)

	def __str__(self):
		return self.nombre+' '+str(self.id)

# clase billetera con los datos necesario para crearla
# faltan los credito y debitos

class BilleteraElectronica (models.Model):
	nombre = models.CharField(max_length = 30, help_text = "Nombre Propio")
	apellido = models.CharField(max_length = 30)
	saldo = models.DecimalField(max_digits=10, decimal_places=2, default = Decimal(0))
	cedula = models.CharField(max_length = 12)
	cedulaTipo = models.CharField(max_length = 1)
	PIN = models.CharField(max_length = 8)
	
	class Meta:
		unique_together = (("cedulaTipo", "cedula"),)
	
	def __str__(self):
		return str(self.id)
	
	def recargar_saldo(self, monto):
		if self.validar_recarga(monto):
			self.saldo += Decimal(monto)
			self.saldo = Decimal(self.saldo).quantize(Decimal('.01'), rounding = ROUND_DOWN)
			self.save()
		
	def validar_recarga(self, monto):
		try:
			if (((self.saldo + Decimal(monto)) <= SMAX) and (monto > 0)):
				return True
			
		except:
			return False
		
		return False
	
	def validar_consumo(self, monto):
		try:
			if ((self.saldo >= Decimal(monto)) and (monto >= 0)):
				return True
		
		except:
			return False
		
		return False
	
	def consumir_saldo(self, monto):
		if self.validar_consumo(monto):
			self.saldo -= Decimal(monto)
			self.saldo = Decimal(self.saldo).quantize(Decimal('.01'), rounding = ROUND_DOWN)
			self.save()
	
class Reserva(models.Model):
	estacionamiento = models.ForeignKey(Estacionamiento)
	inicioReserva   = models.DateTimeField()
	finalReserva    = models.DateTimeField()

	def __str__(self):
		return self.estacionamiento.nombre+' ('+str(self.inicioReserva)+','+str(self.finalReserva)+')'
	
class ConfiguracionSMS(models.Model):
	estacionamiento = models.ForeignKey(Estacionamiento)
	inicioReserva   = models.DateTimeField()
	finalReserva    = models.DateTimeField()

	def __str__(self):
		return self.estacionamiento.nombre+' ('+str(self.inicioReserva)+','+str(self.finalReserva)+')'

class Pago(models.Model):
	fechaTransaccion = models.DateTimeField()
	cedulaTipo       = models.CharField(max_length = 1)
	cedula           = models.CharField(max_length = 10)
	tarjetaTipo      = models.CharField(max_length = 6)
	monto            = models.DecimalField(decimal_places = 2, max_digits = 256)
	reserva          = models.ForeignKey(Reserva, blank = True, null = True)
	id_punto_recarga = models.IntegerField(blank = True, null = True)
	billetera 		 = models.ForeignKey(BilleteraElectronica, blank = True, null = True)
	

	def __str__(self):
		return str(self.id)+" "+str(self.reserva.estacionamiento.nombre)+" "+str(self.cedulaTipo)+"-"+str(self.cedula)

class EsquemaTarifario(models.Model):

	# No se cuantos digitos deberiamos poner
	feriados	 = models.TextField(null=True)
	tarifa         = models.DecimalField(max_digits=20, decimal_places=2)
	tarifa2        = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2)
	tarifaFeriados = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2)
	inicioEspecial = models.TimeField(blank = True, null = True)
	finEspecial    = models.TimeField(blank = True, null = True)
	
	def getFeriados(self):
		return self.feriados.split(",")
	class Meta:
		abstract = True
	def __str__(self):
		return str(self.tarifa)


class TarifaHora(EsquemaTarifario):
	def calcularPrecio(self,horaInicio,horaFinal):
		values=str(horaInicio).split(" ")
		diasferiados=self.feriados.split(",")
		if (values[0] in diasferiados):
			print("Es feriado"+values[0])
		else: print("No es feriado"+values[0])
		a = horaFinal-horaInicio
		a = a.days*24+a.seconds/3600
		a = ceil(a) #  De las horas se calcula el techo de ellas
		return(Decimal(self.tarifa*a).quantize(Decimal('1.00')))
	def tipo(self):
		if (self.tarifaFeriados):
			return("Por Hora con feriados")
		return("Por Hora")

class TarifaMinuto(EsquemaTarifario):
	def calcularPrecio(self,horaInicio,horaFinal):
		minutosNormales = horaFinal-horaInicio
		minutosNormales = minutosNormales.days*24*60+minutosNormales.seconds/60
		
		#Sacamos los feriados
		feriados=self.getFeriados()
		minutosFeriados  = 0
		fechaAnterior = ""
		diaFeriado = False
		tiempoActual       = horaInicio
		minuto             = timedelta(minutes=1)
		while tiempoActual < horaFinal:
			if tiempoActual.date()!=fechaAnterior: # Esta guarda se cumple para el primer ciclo y al cambiar de dia
				#print("Actual:"+str(tiempoActual.date()))
				fechaAnterior = tiempoActual.date()
				diaFeriado=False
				if str(fechaAnterior) in feriados:
					diaFeriado=True
			if (diaFeriado): minutosFeriados += 1
			tiempoActual += minuto
		return ((Decimal(minutosNormales-minutosFeriados)*Decimal(self.tarifa/60))
				+(Decimal(minutosFeriados)*Decimal(self.tarifaFeriados/60))).quantize(Decimal('1.00'))
	def tipo(self):
		if (self.tarifaFeriados):
			return("Por minuto con feriados")
		return("Por minuto")

class TarifaHorayFraccion(EsquemaTarifario):
	def calcularPrecio(self,horaInicio,horaFinal):
		time = horaFinal-horaInicio
		time = time.days*24*3600+time.seconds
		if(time>3600):
			valor = (floor(time/3600)*self.tarifa)
			if((time%3600)==0):
				pass
			elif((time%3600)>1800):
				valor += self.tarifa
			else:
				valor += self.tarifa/2
		else:
			valor = self.tarifa
		return(Decimal(valor).quantize(Decimal('1.00')))

	def tipo(self):
		if (self.tarifaFeriados):
			return("Por Hora y Fraccion con feriados")
		return("Por Hora y Fraccion")

class TarifaFinDeSemana(EsquemaTarifario):
	def calcularPrecio(self,inicio,final):
		# Auxiliares para feriados
		feriados=self.getFeriados()
		minutosFeriados = 0
		fechaAnterior = ""
		diaFeriado=False
		
		minutosNormales    = 0
		minutosFinDeSemana= 0
		tiempoActual       = inicio
		minuto             = timedelta(minutes=1)
		while tiempoActual < final:
			# weekday() devuelve un numero del 0 al 6 tal que
			# 0 = Lunes
			# 1 = Martes
			# ..
			# 5 = Sabado
			# 6 = Domingo
			if tiempoActual.date()!=fechaAnterior: # Esta guarda se cumple para el primer ciclo y al cambiar de dia
				#print("Actual:"+str(tiempoActual.date()))
				fechaAnterior = tiempoActual.date()
				diaFeriado=False
				if str(fechaAnterior) in feriados:
					diaFeriado=True
			if (diaFeriado): minutosFeriados += 1
			else:		
				if tiempoActual.weekday() < 5:
					minutosNormales += 1
				else:
					minutosFinDeSemana += 1
			tiempoActual += minuto
		return Decimal(
			minutosNormales*self.tarifa/60 +
			minutosFinDeSemana*self.tarifa2/60 +
			minutosFeriados*self.tarifaFeriados/60
		).quantize(Decimal('1.00'))

	def tipo(self):
		if (self.tarifaFeriados):
			return("Tarifa diferenciada para fines de semana con feriados")
		return("Tarifa diferenciada para fines de semana")

class TarifaHoraPico(EsquemaTarifario):
	def calcularPrecio(self,reservaInicio,reservaFinal):
		minutosPico  = 0
		minutosValle = 0
		tiempoActual = reservaInicio
		minuto       = timedelta(minutes=1)
		while tiempoActual < reservaFinal:
			horaActual = tiempoActual.time()
			if horaActual >= self.inicioEspecial and horaActual < self.finEspecial:
				minutosPico += 1
			elif horaActual < self.inicioEspecial or horaActual >= self.finEspecial:
				minutosValle += 1
			tiempoActual += minuto
		return Decimal(
			minutosPico*self.tarifa2/60 +
			minutosValle*self.tarifa/60
		).quantize(Decimal('1.00'))

	def tipo(self):
		return("Tarifa diferenciada por hora pico")
