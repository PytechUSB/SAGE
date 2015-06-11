# Archivo con funciones de control para SAGE
from datetime import datetime, timedelta, time
from decimal import Decimal
from collections import OrderedDict
from estacionamientos.models import Propietario, Estacionamiento, Reserva, Pago, BilleteraElectronica, Recargas,Cancelaciones

# chequeo de horarios de extended
def HorarioEstacionamiento(HoraInicio, HoraFin):
	return HoraFin > HoraInicio

def validarHorarioReserva(inicioReserva, finReserva, apertura, cierre):
	if inicioReserva >= finReserva:
		return (False, 'El horario de inicio de reservacion debe ser menor al horario de fin de la reserva.')
	if finReserva - inicioReserva < timedelta(hours=1):
		return (False, 'El tiempo de reserva debe ser al menos de 1 hora.')
	if inicioReserva.date() < datetime.now().date():
		return (False, 'La reserva no puede tener lugar en el pasado.')
	if finReserva.date() > (datetime.now()+timedelta(days=6)).date():
		return (False, 'La reserva debe estar dentro de los próximos 7 días.')
	if apertura.hour==0 and apertura.minute==0 \
		and cierre.hour==23 and cierre.minute==59:
		seven_days=timedelta(days=7)
		if finReserva-inicioReserva<=seven_days :
			return (True,'')
		else:
			return(False,'Se puede reservar un puesto por un maximo de 7 dias.')
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

def marzullo(idEstacionamiento, hIn, hOut, tipoDeVehiculo='Particular', idReservaMovida = None):
	e = Estacionamiento.objects.get(id = idEstacionamiento)
	ocupacion = []
	capacidad = e.obtenerCapacidad(tipoDeVehiculo)
	reservas = e.reserva_set.filter(vehiculoTipo=tipoDeVehiculo)
	pagos_cancelados = Pago.objects.filter(cancelado = True)
	for pago in pagos_cancelados:
		reservas = reservas.exclude(pk = pago.reserva.id)
		
	if idReservaMovida != None:
		print(reservas)
		reservas = reservas.exclude(pk = idReservaMovida)
		print(reservas)
		
	for reserva in reservas:
		ocupacion += [(reserva.inicioReserva, 1), (reserva.finalReserva, -1)]
	ocupacion += [(hIn, 1), (hOut, -1)]
	count = 0
	print(sorted(ocupacion))
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
			ocupacion_por_dia[reserva_inicio.date()] += longitud_reserva.seconds/60+longitud_reserva.days*24*60
			reserva_inicio = final_aux
		longitud_reserva=reserva_final-reserva_inicio
		ocupacion_por_dia[reserva_inicio.date()] += longitud_reserva.seconds/60 + longitud_reserva.days*24*60
			
	return ocupacion_por_dia

def calcular_porcentaje_de_tasa(hora_apertura,hora_cierre, capacidad, ocupacion):
	factor_divisor=timedelta(hours=hora_cierre.hour,minutes=hora_cierre.minute)
	factor_divisor-=timedelta(hours=hora_apertura.hour,minutes=hora_apertura.minute)
	factor_divisor=Decimal(factor_divisor.seconds)/Decimal(60)
	if (hora_apertura==time(0,0) and hora_cierre==time(23,59)):
		factor_divisor+=1 # Se le suma un minuto
	for i in ocupacion.keys():
		ocupacion[i]=(Decimal(ocupacion[i])*100/(factor_divisor*capacidad)).quantize(Decimal('1.0'))
		
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

def billetera_autenticar(identificador, PIN):
	try:
		billetera = BilleteraElectronica.objects.get(pk = identificador)
		if(billetera.PIN == PIN):
			return billetera 
		return None
		
	except(Exception):
		return None
	
def pago_autenticar(identificador, cedulaTipo, cedula):
	try:
		pago = Pago.objects.get(pk = identificador)
		if (pago.cedula == cedula and pago.cedulaTipo == cedulaTipo):
			return pago
		return None
	except:
		return None
	
def asigna_id_unico():
	num_pagos_reservas = len(Pago.objects.all())
	num_recargas = len(Recargas.objects.all())
	num_cancelaciones = len(Cancelaciones.objects.all())
	return (1 + num_pagos_reservas + num_recargas + num_cancelaciones)

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
		
	def getKey(item):
		return item.fechaTransaccion		
		
	return sorted(historial,key=getKey)

def cruceEsquema(idEstacionamiento, hIn, hOut):
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
			monto+=e.tarifaFeriados.calcularPrecio(inicio,final)
		else:
			monto+=e.tarifa.calcularPrecio(inicio,final)
			
		inicio=final
		
		if(final.date() == hOut.date()):
			final = hOut
		else:
			final += timedelta(days=1)
	return monto

def hitenmarzurulli(idEstacionamiento, hIn, hOut):
	""" Siempre se llamara en reservas entre días"""
	e = Estacionamiento.objects.get(id = idEstacionamiento)
	monto = 0
	completo=False
	hora=timedelta(hours=1)
	inicio=hIn
	while hIn<hOut:
		if (inicio.days!=(hIn+hora).days): # Aviso de cambio de dia
			esInicioFeriado=str(inicio.date()) in e.feriados
			if esInicioFeriado^(str(hIn.date()) in e.feriados): #Ambas son distintas
				if hIn+hora>hOut: #Vemos si se pasa de la hora
					if (60-hIn.time().minute)>=hOut.time().minute:
						#se cobra la primera tarifa
						if esInicioFeriado:
							monto+=e.tarifaFeriados.calcularPrecio(inicio,hOut)
						else: monto+=e.tarifa.calcularPrecio(inicio,hOut)
					else:
						#se cobra la segunda tarifa
						if not esInicioFeriado:
							monto+=e.tarifaFeriados.calcularPrecio(inicio,hOut)
						else: monto+=e.tarifa.calcularPrecio(inicio,hOut)
					completo=True
				else:
					if hIn.time().minute<30:
						#se cobra la primera tarifa
						if esInicioFeriado:
							monto+=e.tarifaFeriados.calcularPrecio(inicio,hIn+hora)
						else: monto+=e.tarifa.calcularPrecio(inicio,hIn+hora)
					else:
						#se cobra la segunda tarifa
						if not esInicioFeriado:
							monto+=e.tarifaFeriados.calcularPrecio(inicio,hIn+hora)
						else: monto+=e.tarifa.calcularPrecio(inicio,hIn+hora)
				
				inicio=hIn+hora
		hIn+=hora
	if not completo: #Otro problema de cruce
		esInicioFeriado=str(inicio.date()) in e.feriados
		if esInicioFeriado:
			monto+=e.tarifaFeriados.calcularPrecio(inicio,hOut)
		else: monto+=e.tarifa.calcularPrecio(inicio,hOut)
	return monto
