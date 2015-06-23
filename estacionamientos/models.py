# -*- coding: utf-8 -*-
from django.db import models
from math import ceil, floor
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal, ROUND_DOWN
from datetime import timedelta
SMAX = 10000

class Propietario(models.Model):
    nombres     = models.CharField(max_length = 30)
    apellidos   = models.CharField(max_length = 30)
    cedula      = models.CharField(max_length = 12)
    telefono1   = models.CharField(blank = True, null = True, max_length = 30)
    cedulaTipo  = models.CharField(max_length = 1)

    def __str__(self):
        return self.nombres+' '+self.apellidos
    
    class Meta:
        unique_together=('cedula','cedulaTipo',)

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
    content_type = models.ForeignKey(ContentType, related_name = 'tarifa', null = True)
    object_id    = models.PositiveIntegerField(null = True)
    tarifa       = GenericForeignKey()
    
    # Campos para referenciar al esquema de tarifa para dias feriados
    feriados     = models.TextField(null=True)
    content_type2 = models.ForeignKey(ContentType, related_name = 'tarifaFeriados', null = True)
    object_id2    = models.PositiveIntegerField(null = True)
    tarifaFeriados  = GenericForeignKey(ct_field="content_type2", fk_field="object_id2")
    
    apertura     = models.TimeField(blank = True, null = True)
    cierre       = models.TimeField(blank = True, null = True)
    
    #capacidad para vechiculos personales
    capacidad    = models.IntegerField(blank = True, null = True, default=0)
    #capacidad para motos
    capacidad_M   = models.IntegerField(blank = True, null = True, default=0)
    #capacidad para camiones de carga
    capacidad_C   = models.IntegerField(blank = True, null = True, default=0)
    #capacidad para vehiculos de discapacitados
    capacidad_D   = models.IntegerField(blank = True, null = True, default=0)

    #Horizonte de reservación medido en horas
    horizonte    = models.IntegerField(blank = True, default=168) # 7 dias
    #retorna la capacidd del estacionamiento segun el tipo de vehiculo
    def obtenerCapacidad(self, tipoDeVehiculo):
        puestos = 0
        if tipoDeVehiculo == "Particular":
            puestos  = self.capacidad
        elif tipoDeVehiculo == "Moto":
            puestos  = self.capacidad_M
        elif tipoDeVehiculo == "Camion":
            puestos  = self.capacidad_C
        elif tipoDeVehiculo == "Discapacitado":
            puestos  = self.capacidad_D
        return puestos 
    
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
    vehiculoTipo    = models.CharField(max_length = 15)

    def __str__(self):
        return str(self.id) + ' ' +self.estacionamiento.nombre + ' ' + self.vehiculoTipo+' ('+str(self.inicioReserva)+','+str(self.finalReserva)+')'
    
class ConfiguracionSMS(models.Model):
    estacionamiento = models.ForeignKey(Estacionamiento)
    inicioReserva   = models.DateTimeField()
    finalReserva    = models.DateTimeField()

    def __str__(self):
        return self.estacionamiento.nombre+' ('+str(self.inicioReserva)+','+str(self.finalReserva)+')'

class Pago(models.Model):
    id               = models.IntegerField(primary_key = True)
    fechaTransaccion = models.DateTimeField()
    cedulaTipo       = models.CharField(max_length = 1)
    cedula           = models.CharField(max_length = 10)
    tarjetaTipo      = models.CharField(max_length = 6)
    monto            = models.DecimalField(decimal_places = 2, max_digits = 256)
    reserva          = models.ForeignKey(Reserva)
    cancelado        = models.BooleanField(default = False)
    # Evalua True si la reserva ha sido movida
    fueMovido        = models.BooleanField(default = False)
    nombreUsuario    = models.CharField(max_length = 30)
    apellidoUsuario  = models.CharField(max_length = 30)
    idBilletera      = models.IntegerField(blank = True, null = True)
    # Pago que fue movido y origino esta factura
    facturaMovida    = models.ForeignKey("self", null = True, blank = True)
    
    def __str__(self):
        return str(self.id)+" "+str(self.reserva.estacionamiento.nombre)+" "+str(self.cedulaTipo)+"-"+str(self.cedula)
    
    def cancelar_reserva(self):
        self.cancelado = True
        self.save()
        
    def fue_movido(self):
        self.cancelado = True
        self.fueMovido = True
        self.save() 
        
    def obtener_string(self):
        if self.fueMovido != None:
            return "Reserva Movida"
        
        return "Reservacion"
    
    def obtener_tipo(self):
        return "Pago"
    
    def obtener_monto(self):
        if self.facturaMovida != None:
            if self.facturaMovida.monto <= self.monto:
                return self.monto - self.facturaMovida.monto
            else: return 0
        
        return self.monto
        
    def validar_cancelacion(self, tiempo):
        if ((tiempo < self.reserva.inicioReserva) and (not self.cancelado)):
            return True
        
        return False

class Recargas(models.Model):
    id               = models.IntegerField(primary_key = True)
    fechaTransaccion = models.DateTimeField()
    cedulaTipo       = models.CharField(max_length = 1)
    cedula           = models.CharField(max_length = 10)
    tarjetaTipo      = models.CharField(max_length = 6)
    monto            = models.DecimalField(decimal_places = 2, max_digits = 256)
    billetera        = models.ForeignKey(BilleteraElectronica)
    numTarjeta       = models.CharField(max_length = 16)
    
    def __str__(self):
        return str(self.id)+" "+str(self.billetera.id)+" "+str(self.cedulaTipo)+"-"+str(self.cedula)
    
    def obtener_string(self):
        return "Recarga"
    
    def ultimos_numeros(self):
        arreglo = list(self.numTarjeta)
        resultado = ""
        resultado += str(arreglo[-4])
        resultado += str(arreglo[-3])
        resultado += str(arreglo[-2])
        resultado += str(arreglo[-1])
        return resultado
    
    
class Cancelaciones(models.Model):
    id               = models.IntegerField(primary_key = True)
    pagoCancelado    = models.ForeignKey(Pago)
    billetera        = models.ForeignKey(BilleteraElectronica, blank = True, null = True)
    monto            = models.DecimalField(decimal_places = 2, max_digits = 256)
    fechaTransaccion = models.DateTimeField()
    
    def __str__(self):
        return str(self.id)+" "+str(self.pagoCancelado.id) + " " + str(self.fechaTransaccion)
    
    def obtener_string(self):
        if self.pagoCancelado.fueMovido:
            return "Recarga Reserva Movida"
        
        return "Cancelacion"
    
    def obtener_tipo(self):
        return "Cancelacion"

class EsquemaTarifario(models.Model):
    
    inicioEspecial = models.TimeField(blank = True, null = True)
    finEspecial    = models.TimeField(blank = True, null = True)
    
    # Para Particulares
    tarifa         = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    tarifa2        = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # Para Motos
    tarifa_M         = models.DecimalField(blank = True, null = True, max_digits=20, decimal_places=2, default=Decimal('0.00'))
    tarifa2_M        = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # Para Camiones
    tarifa_C         = models.DecimalField(blank = True, null = True, max_digits=20, decimal_places=2, default=Decimal('0.00'))
    tarifa2_C        = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # Para Discapacitados
    tarifa_D         = models.DecimalField(blank = True, null = True, max_digits=20, decimal_places=2, default=Decimal('0.00'))
    tarifa2_D        = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2, default=Decimal('0.00'))

    #devuelve las tarifas regulares segun el tipo de vehiculo y el tipo de tarifa: tarifa, tarifa2
    def obtenerTarifa(self, tipo, tipoDeVehiculo):
        tarifa  = 0
        # Utilizamos eval() para obtener la variable de clase respectiva y no repetir codigo. Ej: eval('self.tarifa_C').
        if tipoDeVehiculo == "Particular":
            tarifa  = eval('self.'+tipo)
        elif tipoDeVehiculo == "Moto":
            tarifa  = eval('self.'+tipo+'_M')
        elif tipoDeVehiculo == "Camion":
            tarifa  = eval('self.'+tipo+'_C')
        elif tipoDeVehiculo == "Discapacitado":
            tarifa  = eval('self.'+tipo+'_D')
        return tarifa 
   
    class Meta:
        abstract = True
    def __str__(self):
        return str(self.tarifa)

class TarifaHora(EsquemaTarifario):
    def calcularPrecio(self,horaInicio,horaFinal,tipoDeVehiculo):
        tarifa = self.obtenerTarifa('tarifa',tipoDeVehiculo)
        a = horaFinal-horaInicio
        a = a.days*24+a.seconds/3600
        a = ceil(a) #  De las horas se calcula el techo de ellas

        return(Decimal(tarifa*a).quantize(Decimal('1.00')))
    def tipo(self):
        return("Por Hora")

class TarifaMinuto(EsquemaTarifario):
    def calcularPrecio(self,horaInicio,horaFinal,tipoDeVehiculo):
        tarifa = self.obtenerTarifa('tarifa',tipoDeVehiculo)
        minutes = horaFinal-horaInicio
        minutes = minutes.days*24*60+minutes.seconds/60
        return (Decimal(minutes)*Decimal(tarifa/60)).quantize(Decimal('1.00'))
    def tipo(self):
        return("Por Minuto")

class TarifaHorayFraccion(EsquemaTarifario):
    def calcularPrecio(self,horaInicio,horaFinal,tipoDeVehiculo):
        tarifa = self.obtenerTarifa('tarifa',tipoDeVehiculo)
        time = horaFinal-horaInicio
        time = time.days*24*3600+time.seconds
        if(time>3600):
            valor = (floor(time/3600)*tarifa)
            if((time%3600)==0):
                pass
            elif((time%3600)>1800):
                valor += tarifa
            else:
                valor += tarifa/2
        else:
            valor = tarifa
        return(Decimal(valor).quantize(Decimal('1.00')))

    def tipo(self):
        return("Por Hora y Fraccion")

class TarifaFinDeSemana(EsquemaTarifario):
    def calcularPrecio(self,inicio,final,tipoDeVehiculo):
        tarifa = self.obtenerTarifa('tarifa',tipoDeVehiculo)
        tarifa2 = self.obtenerTarifa('tarifa2',tipoDeVehiculo)
        minutosNormales    = 0
        minutosFinDeSemana = 0
        tiempoActual       = inicio
        minuto             = timedelta(minutes=1)
        while tiempoActual < final:
            # weekday() devuelve un numero del 0 al 6 tal que
            # 0 = Lunes
            # 1 = Martes
            # ..
            # 5 = Sabado
            # 6 = Domingo
            if tiempoActual.weekday() < 5:
                minutosNormales += 1
            else:
                minutosFinDeSemana += 1
            tiempoActual += minuto
        return Decimal(
            minutosNormales*tarifa/60 +
            minutosFinDeSemana*tarifa2/60
        ).quantize(Decimal('1.00'))

    def tipo(self):
        return("Tarifa diferenciada para fines de semana")

class TarifaHoraPico(EsquemaTarifario):
    def calcularPrecio(self,reservaInicio,reservaFinal,tipoDeVehiculo):
        tarifa = self.obtenerTarifa('tarifa',tipoDeVehiculo)
        tarifa2 = self.obtenerTarifa('tarifa2',tipoDeVehiculo)
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
            minutosPico*tarifa2/60 +
            minutosValle*tarifa/60
        ).quantize(Decimal('1.00'))

    def tipo(self):
        return("Tarifa diferenciada por hora pico")
