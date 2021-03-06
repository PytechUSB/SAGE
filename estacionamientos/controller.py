# Archivo con funciones de control para SAGE
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from estacionamientos.models import (
	Estacionamiento, 
	Pago, 
	BilleteraElectronica, 
	Recargas,Cancelaciones,
	PagoOperacionesEspeciales
)

# Chequeo de horarios de extended
def HorarioEstacionamiento(HoraInicio, HoraFin):
	return HoraFin > HoraInicio

# Validacion de la hora y fecha de la reserva
def validarHorarioReserva(inicioReserva, finReserva, apertura, cierre, horizonte = 168):
	inicioReserva=inicioReserva.replace(second=0,microsecond=0)
	finReserva=finReserva.replace(second=0,microsecond=0)
	if inicioReserva >= finReserva:
		return (False, 'El horario de inicio de reservacion debe ser menor al horario de fin de la reserva.')
	if finReserva - inicioReserva < timedelta(hours=1):
		return (False, 'El tiempo de reserva debe ser al menos de 1 hora.')
	if inicioReserva < datetime.now().replace(second=0,microsecond=0):
		return (False, 'La reserva no puede tener lugar en el pasado.')
	
	if apertura.hour==0 and apertura.minute==0 \
		and cierre.hour==23 and cierre.minute==59:
		fifteen_days=timedelta(days=15)
		if finReserva-inicioReserva<=fifteen_days:
			if finReserva > datetime.now().replace(second=0,microsecond=0)+timedelta(hours=horizonte):
				return (False, 'La reserva debe estar dentro del horizonte de reservacion.')
			return (True,'')
			
		else:
			return(False,'Se puede reservar un puesto por un maximo de 15 dias dependiendo horizonte de reservacion.')
		
	if finReserva > datetime.now().replace(second=0,microsecond=0)+timedelta(hours=horizonte):
		return (False, 'La reserva debe estar dentro del horizonte de reservacion.')
	
	else:
		hora_inicio = time(hour = inicioReserva.hour, minute = inicioReserva.minute)
		hora_final  = time(hour = finReserva.hour   , minute = finReserva.minute)
		if hora_inicio<apertura:
			return (False, 'El horario de inicio de reserva debe estar en un horario válido.')
		if hora_final > cierre:
			return (False, 'El horario de fin de la reserva debe estar en un horario válido.')
		if inicioReserva.date()!=finReserva.date():
			return (False, 'No puede haber reservas entre dos dias distintos')
		return (True,'')
	
# Validacion de la hora y fecha de la nueva reserva movida
def validarHorarioReservaMover(inicioReserva, finReserva, apertura, cierre, horizonte = 168):
	inicioReserva=inicioReserva.replace(second=0,microsecond=0)
	finReserva=finReserva.replace(second=0,microsecond=0)
	if inicioReserva >= finReserva:
		return (False, 'El horario de inicio de reservacion debe ser menor al horario de fin de la reserva.')
	if finReserva - inicioReserva < timedelta(hours=1):
		return (False, 'El tiempo de reserva debe ser al menos de 1 hora.')
	if inicioReserva < datetime.now().replace(second=0,microsecond=0):
		return (False, 'La reserva no puede tener lugar en el pasado.')
	
	if apertura.hour==0 and apertura.minute==0 \
		and cierre.hour==23 and cierre.minute==59:
		fifteen_days=timedelta(days=15)
		if finReserva-inicioReserva<=fifteen_days:
			if (porcentajeReservaDentroHorizonte(inicioReserva, finReserva, horizonte) < 50 or 
			   finReserva > datetime.now() + timedelta(days = 15)) :
				return (False, 'Una mayor proporcion de la reserva debe estar dentro del horizonte de reservacion.')
			return (True,'')
		
		else:
			return(False,'Se puede reservar un puesto por un maximo de 15 dias dependiendo horizonte de reservacion.')
		
	if finReserva > datetime.now().replace(second=0,microsecond=0)+timedelta(hours=horizonte):
		if (porcentajeReservaDentroHorizonte(inicioReserva, finReserva, horizonte) < 50  or 
		   finReserva > datetime.now() + timedelta(days = 15)):
			return (False, 'Una mayor proporcion de la reserva debe estar dentro del horizonte de reservacion.')
	
	else:
		hora_inicio = time(hour = inicioReserva.hour, minute = inicioReserva.minute)
		hora_final  = time(hour = finReserva.hour   , minute = finReserva.minute)
		if hora_inicio<apertura:
			return (False, 'El horario de inicio de reserva debe estar en un horario válido.')
		if hora_final > cierre:
			return (False, 'El horario de fin de la reserva debe estar en un horario válido.')
		if inicioReserva.date()!=finReserva.date():
			return (False, 'No puede haber reservas entre dos dias distintos')
		return (True,'')


# Calcula el porcentaje de la reserva que queda dentro del horizonte cuando se aplica mover	
def porcentajeReservaDentroHorizonte(inicioReserva, finReserva, horizonte):
	total_reserva = (finReserva - inicioReserva).total_seconds()
	horizonte = datetime.now().replace(second = 0, microsecond = 0) + timedelta(hours = horizonte)
	if inicioReserva < horizonte:
		if finReserva > horizonte:
			reservaEnHorizonte = (horizonte - inicioReserva).total_seconds()
			porcentaje = Decimal(Decimal(reservaEnHorizonte * 100) / Decimal(total_reserva)).quantize(Decimal('1.0'))
			return porcentaje
		
		else:
			return 100
	
	else:
		return 0
	
# Calcula el monto de una reserva
def calcularMonto(idEstacionamiento, hIn, hOut, tipoDeVehiculo='Particular'):
	e = Estacionamiento.objects.get(id = idEstacionamiento)
	monto  = 0
	inicio = hIn
	#revisa si la hora de inicio y finalizacion corresponden al mismo dia
	if(inicio.date() == hOut.date()):
		final = hOut
	else:
		final  = datetime.combine(inicio.date() + timedelta(days=1), time(0,0))
	#calcula el monto segun el esquema y el dia
	while inicio<hOut:
		if(e.tarifaFeriados and (str(inicio.date()) in e.feriados)):
			monto+=e.tarifaFeriados.calcularPrecio(inicio,final, tipoDeVehiculo)
		else:
			monto+=e.tarifa.calcularPrecio(inicio,final, tipoDeVehiculo)

		inicio=final
		if(final.date() == hOut.date()):
			final = hOut
		else:
			final += timedelta(days=1)
	return monto

# Determina si hay o no puestos disponibles en un estacionamiento y a una fecha y hora dada
def marzullo(idEstacionamiento, hIn, hOut, tipoDeVehiculo='Particular', idReservaMovida = None):
	e = Estacionamiento.objects.get(id = idEstacionamiento)
	ocupacion = []
	capacidad = e.obtenerCapacidad(tipoDeVehiculo)
	reservas = e.reserva_set.filter(vehiculoTipo=tipoDeVehiculo)
	pagos_cancelados = Pago.objects.filter(cancelado = True)
	for pago in pagos_cancelados:
		reservas = reservas.exclude(pk = pago.reserva.id)
		
	if idReservaMovida != None:
		reservas = reservas.exclude(pk = idReservaMovida)
		
	for reserva in reservas:
		ocupacion += [(reserva.inicioReserva, 1), (reserva.finalReserva, -1)]
	ocupacion += [(hIn, 1), (hOut, -1)]
	count = 0
	for r in sorted(ocupacion):
		count += r[1]
		if count > capacidad:
			return False
	return True


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[-1].strip()
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

# Calcula la tasa de reservaciones
def tasa_reservaciones(id_estacionamiento,prt=False):
	e = Estacionamiento.objects.get(id = id_estacionamiento)
	ahora = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
	reservas_filtradas = e.reserva_set.filter(finalReserva__gt=ahora)
	pagos_cancelados = Pago.objects.filter(cancelado = True)
	for cancelados in pagos_cancelados:
		reservas_filtradas = reservas_filtradas.exclude(id = cancelados.reserva.id)
		
	lista_fechas=[(ahora+timedelta(i)).date() for i in range(7)]
	lista_valores=[0 for i in range(7)]
	ocupacion_por_dia = OrderedDict(zip(lista_fechas,lista_valores))
	UN_DIA = timedelta(days = 1)
	
	for reserva in reservas_filtradas:
		# Caso del inicio de la reserva
		if (reserva.inicioReserva < ahora):
			reserva_inicio = ahora
		else:
			reserva_inicio = reserva.inicioReserva
		reserva_final = reserva.finalReserva
		final_aux=reserva_inicio.replace(hour=0,minute=0,second=0,microsecond=0)
		while (reserva_final.date()>reserva_inicio.date()): 
			final_aux+=UN_DIA
			longitud_reserva = final_aux-reserva_inicio
			try:
				ocupacion_por_dia[reserva_inicio.date()] += longitud_reserva.seconds/60 + longitud_reserva.days*24*60
			except:
				ocupacion_por_dia [reserva_inicio.date()] = longitud_reserva.seconds/60 + longitud_reserva.days*24*60
			reserva_inicio = final_aux
		longitud_reserva=reserva_final-reserva_inicio
		try:
			ocupacion_por_dia[reserva_inicio.date()] += longitud_reserva.seconds/60 + longitud_reserva.days*24*60
		except:
			ocupacion_por_dia [reserva_inicio.date()] = longitud_reserva.seconds/60 + longitud_reserva.days*24*60
	return ocupacion_por_dia

# Calcula el porcentaje de ocupacion de un estacionamiento
def calcular_porcentaje_de_tasa(hora_apertura,hora_cierre, capacidad, ocupacion):
	if capacidad > 0:
		factor_divisor=timedelta(hours=hora_cierre.hour,minutes=hora_cierre.minute)
		factor_divisor-=timedelta(hours=hora_apertura.hour,minutes=hora_apertura.minute)
		factor_divisor=Decimal(factor_divisor.seconds)/Decimal(60)
		if (hora_apertura==time(0,0) and hora_cierre==time(23,59)):
			factor_divisor+=1 # Se le suma un minuto
		for i in ocupacion.keys():
			ocupacion[i]=(Decimal(ocupacion[i])*100/(factor_divisor*capacidad)).quantize(Decimal('1.0'))
			
	else:
		for i in ocupacion.keys():
			ocupacion[i] = 0

# Calcula los ingresos de un estacionamiento dado		
def consultar_ingresos(rif):
	listaEstacionamientos = Estacionamiento.objects.filter(rif = rif)
	ingresoTotal = 0
	listaIngresos = []
	
	for estacionamiento in listaEstacionamientos:
		listaFacturas = Pago.objects.exclude(cancelado = True)
		listaFacturas = listaFacturas.filter(
			reserva__estacionamiento__nombre = estacionamiento.nombre
		)
		ingreso = [estacionamiento.nombre, 0]
		for factura in listaFacturas:
			ingreso[1] += factura.monto
		listaIngresos += [ingreso]
		ingresoTotal += ingreso[1]
		
	return listaIngresos, ingresoTotal

# Valida que en la base de datos haya una billetera con identificador y PIN dados
def billetera_autenticar(identificador, PIN):
	try:
		billetera = BilleteraElectronica.objects.get(pk = identificador)
		if(billetera.PIN == PIN):
			return billetera 
		return None
		
	except(Exception):
		return None

# Valida la existencia de un pago y si la cedula corresponde con la registrada	
def pago_autenticar(identificador, cedulaTipo, cedula):
	try:
		pago = Pago.objects.get(pk = identificador)
		if (pago.cedula == cedula and pago.cedulaTipo == cedulaTipo):
			return pago
		return None
	except:
		return None
	
# Genera el id de cada una de las facturas del sistema	
def asigna_id_unico():
	num_pagos_reservas = len(Pago.objects.all())
	num_recargas = len(Recargas.objects.all())
	num_cancelaciones = len(Cancelaciones.objects.all())
	num_opEspeciales = len(PagoOperacionesEspeciales.objects.all())
	return (1 + num_pagos_reservas + num_recargas + num_cancelaciones + num_opEspeciales)

# Busca las operaciones asociadas a una billetera dada
def buscar_historial_billetera(identificador):
	historial = []
	lista_recargas = Recargas.objects.filter(billetera = identificador)
	for rec in lista_recargas:
		historial.append(rec)
		
	lista_cancelaciones = Cancelaciones.objects.filter(billetera = identificador)	
	for can in lista_cancelaciones:
		historial.append(can)
	
	lista_pagos = Pago.objects.filter(idBilletera = identificador)
	for pag in lista_pagos:
		historial.append(pag)
		
	lista_opEspeciales = PagoOperacionesEspeciales.objects.filter(billetera = identificador)
	for opEsp in lista_opEspeciales:
		historial.append(opEsp)
		
	def getKey(item):
		return item.fechaTransaccion	
		
	return sorted(historial,key=getKey) 
