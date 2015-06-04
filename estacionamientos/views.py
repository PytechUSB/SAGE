# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import urllib
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.dateparse import parse_datetime
from urllib.parse import urlencode
from matplotlib import pyplot
from decimal import Decimal
from collections import OrderedDict
from django.db import transaction
from django.db.utils import IntegrityError

from datetime import datetime, timedelta

from estacionamientos.controller import (
    HorarioEstacionamiento,
    validarHorarioReserva,
    marzullo,
    get_client_ip,
    tasa_reservaciones,
    calcular_porcentaje_de_tasa,
    consultar_ingresos,
    billetera_autenticar,
    pago_autenticar,
    asigna_id_unico
)

from estacionamientos.forms import (
    EstacionamientoExtendedForm,
    EstacionamientoForm,
    PropietarioForm,
    ReservaForm,
    PagoForm,
    RifForm,
    CedulaForm,
    BilleteraForm,
    BilleteraPagoForm,
    authBilleteraForm,
    CancelaReservaForm
)
from estacionamientos.models import (
    Propietario,
    Estacionamiento,
    BilleteraElectronica,
    Recargas,
    Reserva,
    Pago,
    TarifaHora,
    TarifaMinuto,
    TarifaHorayFraccion,
    TarifaFinDeSemana,
    TarifaHoraPico, 
    Cancelaciones)

# Vista para procesar los propietarios
def propietario_all(request):
    propietarios = Propietario.objects.all()
    estacionamientos = Estacionamiento.objects.all()

    # Si es un GET, mandamos un formulario vacio
    if request.method == 'GET':
        form = PropietarioForm()

    # Si es POST, se verifica la información recibida
    elif request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        form = PropietarioForm(request.POST)

        # Parte de la entrega era limitar la cantidad maxima de
        # estacionamientos a 5
        if len(propietarios) >= 5 or 5 - len(estacionamientos) <= 0:
            return render(
                request, 'template-mensaje.html',
                { 'color'   : 'red'
                , 'mensaje' : 'No se pueden agregar más propietarios.'
                }
            )

        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
            obj = Propietario(
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                cedula=form.cleaned_data['cedula'],
                telefono1=form.cleaned_data['telefono_1']
            )     
            try:
                obj.save()
            except:
                return render(
                    request, 'template-mensaje.html',
                    { 'color'   : 'red'
                    , 'mensaje' : 'Cédula ya existente'
                    }
                )
            # Recargamos los propietarios ya que acabamos de agregar
            propietarios = Propietario.objects.all()
            form = PropietarioForm()

    return render(
        request,
        'Propietario/propietario-menu.html',
        { 'form': form
        , 'propietarios': propietarios
        , 'estacionamientos': estacionamientos
        }
    )

def propietario_edit(request, _id):
    estacionamientos = Estacionamiento.objects.all()
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        propietario = Propietario.objects.get(id=_id)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'GET':
        form_data = {
            'nombres' : propietario.nombres,
            'apellidos' : propietario.apellidos,
            'cedula' : propietario.cedula,
            'telefono1' : propietario.telefono1 
        }
        form = PropietarioForm(data=form_data)

    elif request.method == 'POST':
        # Leemos el formulario
        form = PropietarioForm(request.POST)
        # Si el formulario
        if form.is_valid():
            try:
                Propietario.objects.filter(id=_id).update(
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                cedula=form.cleaned_data['cedula'],
                telefono1=form.cleaned_data['telefono_1']
            )
            except:
                return render(
                    request, 'template-mensaje.html',
                    { 'color'   : 'red'
                    , 'mensaje' : 'Cédula ya existente'
                    }
                ) 
    
    propietario = Propietario.objects.get(id=_id)
    return render(
        request,
        'Propietario/detalle-propietario.html',
        { 'estacionamientos': estacionamientos,
          'propietario': propietario,
          'form': form
        }
    )

# Usamos esta vista para procesar todos los estacionamientos
def estacionamientos_all(request):
    estacionamientos = Estacionamiento.objects.all()
    propietarios = Propietario.objects.all()
    
    # Si es un GET, mandamos un formulario vacio
    if request.method == 'GET':
        form = EstacionamientoForm()

    # Si es POST, se verifica la información recibida
    elif request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        form = EstacionamientoForm(request.POST)

        # Parte de la entrega era limitar la cantidad maxima de
        # estacionamientos a 5
        if len(estacionamientos) >= 5:
            return render(
                request, 'template-mensaje.html',
                { 'color'   : 'red'
                , 'mensaje' : 'No se pueden agregar más estacionamientos'
                }
            )

        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
            obj = Estacionamiento(
                nombre=form.cleaned_data['nombre'],
                direccion=form.cleaned_data['direccion'],
                rif=form.cleaned_data['rif'],
                telefono1=form.cleaned_data['telefono_1'],
                telefono2=form.cleaned_data['telefono_2'],
                telefono3=form.cleaned_data['telefono_3'],
                email1=form.cleaned_data['email_1'],
                email2=form.cleaned_data['email_2'],
                propietario=form.cleaned_data['propietario']
            )
            obj.save()
            # Recargamos los estacionamientos ya que acabamos de agregar
            estacionamientos = Estacionamiento.objects.all()
            form = EstacionamientoForm()

    return render(
        request,
        'catalogo-estacionamientos.html',
        { 'form': form
        , 'propietarios': propietarios
        , 'estacionamientos': estacionamientos
        }
    )

def estacionamiento_detail(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id=_id)
    except ObjectDoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        
        if estacionamiento.tarifa:
            form_data = {
                'horarioin' : estacionamiento.apertura,
                'horarioout' : estacionamiento.cierre,
                'tarifa' : estacionamiento.tarifa.tarifa,
                'tarifa2' : estacionamiento.tarifa.tarifa2,
                'inicioTarifa2' : estacionamiento.tarifa.inicioEspecial,
                'finTarifa2' : estacionamiento.tarifa.finEspecial,
                'puestos' : estacionamiento.capacidad,
                'esquema' : estacionamiento.tarifa.__class__.__name__,
                'feriados' : estacionamiento.feriados
            }
            if estacionamiento.tarifaFeriados:
                form_data.update({
                    'tarifaFeriados' : estacionamiento.tarifaFeriados.tarifa,
                    'tarifaFeriados2' : estacionamiento.tarifaFeriados.tarifa2,
                    'inicioTarifaFeriados2' : estacionamiento.tarifaFeriados.inicioEspecial,
                    'finTarifaFeriados2' : estacionamiento.tarifaFeriados.finEspecial,
                    'esquemaFeriados' : estacionamiento.tarifaFeriados.__class__.__name__
                })
            form = EstacionamientoExtendedForm(data=form_data)
        else:
            form = EstacionamientoExtendedForm()

    elif request.method == 'POST':
        # Leemos el formulario
        form = EstacionamientoExtendedForm(request.POST)
        # Si el formulario
        if form.is_valid():
            horaIn = form.cleaned_data['horarioin']
            horaOut = form.cleaned_data['horarioout']
            tarifa = form.cleaned_data['tarifa']
            tipo = form.cleaned_data['esquema']
            inicioTarifa2 = form.cleaned_data['inicioTarifa2']
            finTarifa2 = form.cleaned_data['finTarifa2']
            tarifa2 = form.cleaned_data['tarifa2']
            feriados = form.cleaned_data['feriados']
            tipo2 = form.cleaned_data['esquemaFeriados']
            inicioTarifaFeriados = form.cleaned_data['inicioTarifaFeriados']
            finTarifaFeriados = form.cleaned_data['finTarifaFeriados']
            tarifaFeriados2 = form.cleaned_data['tarifaFeriados2']
            tarifaFeriados = form.cleaned_data['tarifaFeriados']
            
            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            if not HorarioEstacionamiento(horaIn, horaOut):
                return render(
                    request,
                    'template-mensaje.html',
                    { 'color':'red'
                    , 'mensaje': 'El horario de apertura debe ser menor al horario de cierre'
                    }
                )

            esquemaTarifa = eval(tipo)(
                tarifa=tarifa,
                tarifa2=tarifa2,
                inicioEspecial=inicioTarifa2,
                finEspecial=finTarifa2
            )
            if (tarifaFeriados):
                esquemaTarifaFeriados = eval(tipo2)(
                    tarifa=tarifaFeriados,
                    tarifa2=tarifaFeriados2,
                    inicioEspecial=inicioTarifaFeriados,
                    finEspecial=finTarifaFeriados
                )
                esquemaTarifaFeriados.save()
                estacionamiento.tarifaFeriados = esquemaTarifaFeriados
            else:
                if (estacionamiento.tarifaFeriados):
                    estacionamiento.tarifaFeriados.delete()
            esquemaTarifa.save()
            
            # debería funcionar con excepciones
            estacionamiento.feriados = feriados
            estacionamiento.tarifa = esquemaTarifa
            estacionamiento.apertura = horaIn
            estacionamiento.cierre = horaOut
            estacionamiento.capacidad = form.cleaned_data['puestos']

            estacionamiento.save()
            
    return render(
        request,
        'detalle-estacionamiento.html',
        { 'form': form
        , 'estacionamiento': estacionamiento
        }
    )

def estacionamiento_edit(request, _id):
    # estacionamientos = Estacionamiento.objects.all()
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id=_id)
    except ObjectDoesNotExist:
        raise Http404

    form = CedulaForm()
    if request.method == 'POST':
        form = CedulaForm(request.POST)
        if form.is_valid():

            cedula = form.cleaned_data['cedula']
            try:
                propietario = Propietario.objects.get(cedula=cedula)
                Estacionamiento.objects.filter(id=_id).update(
                    propietario=propietario
                    )
            except:
                return render(
                    request, 'Propietario/cambiar-propietario.html',
                    { 'color'   : 'red'
                    , 'estacionamiento': estacionamiento
                    , 'mensajeR' : 'No existe tal propietario'
                    }
                )
            return render(
                    request, 'Propietario/cambiar-propietario.html',
                    { 'color'   : 'green'
                    , 'estacionamiento': estacionamiento
                    , 'mensajeG' : 'Se ha cambiado exitosamente'
                    }
                )
            
            
    return render(
        request,
        'Propietario/cambiar-propietario.html',
        { 'form': form
        , 'estacionamiento': estacionamiento
        }
    )

def estacionamiento_reserva(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id=_id)
    except ObjectDoesNotExist:
        raise Http404

    # Verificamos que el estacionamiento este parametrizado
    if (estacionamiento.apertura is None):
        return HttpResponse(status=403)  # Esta prohibido entrar aun

    # Si se hace un GET renderizamos los estacionamientos con su formulario
    if request.method == 'GET':
        form = ReservaForm()

    # Si es un POST estan mandando un request
    elif request.method == 'POST':
        form = ReservaForm(request.POST)
        # Verificamos si es valido con los validadores del formulario
        if form.is_valid():

            inicioReserva = form.cleaned_data['inicio']
            finalReserva = form.cleaned_data['final']

            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            m_validado = validarHorarioReserva(
                inicioReserva,
                finalReserva,
                estacionamiento.apertura,
                estacionamiento.cierre,
            )

            # Si no es valido devolvemos el request
            if not m_validado[0]:
                return render(
                    request,
                    'template-mensaje.html',
                    { 'color'  :'red'
                    , 'mensaje': m_validado[1]
                    }
                )

            if marzullo(_id, inicioReserva, finalReserva):
                reservaFinal = Reserva(
                    estacionamiento=estacionamiento,
                    inicioReserva=inicioReserva,
                    finalReserva=finalReserva,
                )
                print(inicioReserva)
                
                diaFeriado = False
                feriados = estacionamiento.feriados.split(',')
                dia = inicioReserva.date()
                if(str(dia) in feriados):
                    diaFeriado = True
                    
                if(estacionamiento.tarifaFeriados and diaFeriado):
                    monto = Decimal(
                        estacionamiento.tarifaFeriados.calcularPrecio(
                            inicioReserva, finalReserva
                        )
                    )

                    request.session['monto'] = float(
                        estacionamiento.tarifaFeriados.calcularPrecio(
                            inicioReserva,
                            finalReserva
                        )
                    )
                else:
                    monto = Decimal(
                        estacionamiento.tarifa.calcularPrecio(
                            inicioReserva, finalReserva
                        )
                    )
                    request.session['monto'] = float(
                        estacionamiento.tarifa.calcularPrecio(
                            inicioReserva,
                            finalReserva
                        )
                    )
                    
                request.session['finalReservaHora'] = finalReserva.hour
                request.session['finalReservaMinuto'] = finalReserva.minute
                request.session['inicioReservaHora'] = inicioReserva.hour
                request.session['inicioReservaMinuto'] = inicioReserva.minute
                request.session['anioinicial'] = inicioReserva.year
                request.session['mesinicial'] = inicioReserva.month
                request.session['diainicial'] = inicioReserva.day
                request.session['aniofinal'] = finalReserva.year
                request.session['mesfinal'] = finalReserva.month
                request.session['diafinal'] = finalReserva.day
                return render(
                    request,
                    'confirmar.html',
                    { 'id'      : _id
                    , 'monto'   : monto
                    , 'reserva' : reservaFinal
                    , 'color'   : 'green'
                    , 'mensaje' : 'Existe un puesto disponible'
                    }
                )
            else:
                # Cambiar mensaje
                return render(
                    request,
                    'template-mensaje.html',
                    {'color'   : 'red'
                    , 'mensaje' : 'No hay un puesto disponible para ese horario'
                    }
                )

    return render(
        request,
        'reserva.html',
        { 'form': form
        , 'estacionamiento': estacionamiento
        }
    )

def pago_reserva_aux(request, form, monto, estacionamiento):
    inicioReserva = datetime(
        year   = request.session['anioinicial'],
        month  = request.session['mesinicial'],
        day    = request.session['diainicial'],
        hour   = request.session['inicioReservaHora'],
        minute = request.session['inicioReservaMinuto']
    )

    finalReserva  = datetime(
        year   = request.session['aniofinal'],
        month  = request.session['mesfinal'],
        day    = request.session['diafinal'],
        hour   = request.session['finalReservaHora'],
        minute = request.session['finalReservaMinuto']
    )

    reservaFinal = Reserva(
        estacionamiento = estacionamiento,
        inicioReserva   = inicioReserva,
        finalReserva    = finalReserva,
    )

    # Se guarda la reserva en la base de datos
    reservaFinal.save()
    pago = Pago(
        id = asigna_id_unico(),
        fechaTransaccion = datetime.now(),
        cedula           = form.cleaned_data['cedula'],
        cedulaTipo       = form.cleaned_data['cedulaTipo'],
        monto            = monto,
        tarjetaTipo      = form.cleaned_data['tarjetaTipo'],
        reserva          = reservaFinal,
    )

    return pago


def estacionamiento_pago(request,_id):
    form = PagoForm()
    
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    
    if (estacionamiento.apertura is None):
        return HttpResponse(status = 403) # No esta permitido acceder a esta vista aun
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            monto = Decimal(request.session['monto']).quantize(Decimal('1.00'))
            if (form.cleaned_data['tarjetaTipo'] == 'Billetera Electronica'):
                billeteraE = billetera_autenticar(form.cleaned_data['ID'], form.cleaned_data['PIN'])
                
                if (billeteraE == None):
                    return render(
                        request, 'mensaje.html',
                        {'color' : 'red'
                        , 'mensaje' : 'Autenticacion Denegada'
                        }
                    )
                    
                else:
                    if(not billeteraE.validar_consumo(monto)):
                        return render(
                            request, 'mensaje.html',
                            {'color' : 'red'
                            , 'mensaje' : 'Saldo Insuficiente'
                            }
                        ) 
                        
                    else:
                        pago = pago_reserva_aux(request, form, monto, estacionamiento)
                        pago.save()
                        billeteraE.consumir_saldo(monto)
                        if (billeteraE.saldo == 0):
                            return render(
                                request,
                                'pago.html',
                                { "id"      : _id
                                , "pago"    : pago
                                , "color"   : "green"
                                , 'mensaje' : "Se realizo el pago de reserva satisfactoriamente."
                                , 'color2'  : 'red'
                                , 'mensaje2': 'Se recomienda recargar la billetera.' 
                                }
                            )
                            
                        else:
                            return render(
                                request,
                                'pago.html',
                                { "id"      : _id
                                , "pago"    : pago
                                , "color"   : "green"
                                , 'mensaje' : "Se realizo el pago de reserva satisfactoriamente."
                                }
                            )
                        
            
            
            else:
                pago = pago_reserva_aux(request, form, monto, estacionamiento)
                pago.save()
                return render(
                    request,
                    'pago.html',
                    { "id"      : _id
                    , "pago"    : pago
                    , "color"   : "green"
                    , 'mensaje' : "Se realizo el pago de reserva satisfactoriamente."
                    }
                )

    return render(
        request,
        'pago.html',
        { 'form' : form }
    )

def estacionamiento_ingreso(request):
    form = RifForm()
    if request.method == 'POST':
        form = RifForm(request.POST)
        if form.is_valid():

            rif = form.cleaned_data['rif']
            listaIngresos, ingresoTotal = consultar_ingresos(rif)

            return render(
                request,
                'consultar-ingreso.html',
                { "ingresoTotal"  : ingresoTotal
                , "listaIngresos" : listaIngresos
                , "form"          : form
                }
            )

    return render(
        request,
        'consultar-ingreso.html',
        { "form" : form }
    )

def estacionamiento_consulta_reserva(request):
    form = CedulaForm()
    if request.method == 'POST':
        form = CedulaForm(request.POST)
        if form.is_valid():

            cedula        = form.cleaned_data['cedula']
            facturas      = Pago.objects.filter(cedula = cedula)
            facturas      = facturas.exclude(cancelado = True)
            listaFacturas = []

            listaFacturas = sorted(
                list(facturas),
                key = lambda r: r.reserva.inicioReserva
            )
            return render(
                request,
                'consultar-reservas.html',
                { "listaFacturas" : listaFacturas
                , "form"          : form
                }
            )
    return render(
        request,
        'consultar-reservas.html',
        { "form" : form }
    )

def receive_sms(request):
    ip = get_client_ip(request) # Busca el IP del telefono donde esta montado el SMS Gateway
    port = '8000' # Puerto del telefono donde esta montado el SMS Gateway
    phone = request.GET.get('phone', False)
    sms = request.GET.get('text', False)
    if (not sms or not phone):
        return HttpResponse(status=400) # Bad request
    
    phone = urllib.parse.quote(str(phone)) # Codificacion porcentaje del numero de telefono recibido
    
    # Tratamiento del texto recibido
    try:
        sms = sms.split(' ')
        id_sms = int(sms[0])
        inicio_reserva = sms[1] + ' ' + sms[2]
        final_reserva = sms[3] + ' ' + sms[4]
        inicio_reserva = parse_datetime(inicio_reserva)
        final_reserva = parse_datetime(final_reserva)
    except:
        return HttpResponse(status=400) # Bad request
    
    # Validacion del id de estacionamiento recibido por SMS
    try:
        estacionamiento = Estacionamiento.objects.get(id = id_sms)
    except ObjectDoesNotExist:
        text = 'No existe el estacionamiento ' + str(id_sms) + '.'
        text = urllib.parse.quote(str(text))
        urllib.request.urlopen('http://{0}:{1}/sendsms?phone={2}&text={3}&password='.format(ip, port, phone, text))
        return HttpResponse('No existe el estacionamiento ' + str(id_sms) + '.')
    
    # Validacion de las dos fechas recibidas por SMS
    m_validado = validarHorarioReserva(
        inicio_reserva,
        final_reserva,
        estacionamiento.apertura,
        estacionamiento.cierre,
    )
    if m_validado[0]:
        '''reserva_sms = Reserva(
            estacionamiento = estacionamiento,
            inicioReserva   = inicio_reserva,
            finalReserva    = final_reserva,
        )
        reserva_sms.save()'''
        text = 'Se realizó la reserva satisfactoriamente.'
        text = urllib.parse.quote(str(text))
        urllib.request.urlopen('http://{0}:{1}/sendsms?phone={2}&text={3}&password='.format(ip, port, phone, text))
    else:
        text = m_validado[1]
        text = urllib.parse.quote(str(text))
        urllib.request.urlopen('http://{0}:{1}/sendsms?phone={2}&text={3}&password='.format(ip, port, phone, text))
        return HttpResponse(m_validado[1])
    
    return HttpResponse('')
    
def tasa_de_reservacion(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        raise Http404
    if (estacionamiento.apertura is None):
        return render(
            request, 'template-mensaje.html',
            { 'color'   : 'red'
            , 'mensaje' : 'Se debe parametrizar el estacionamiento primero.'
            }
        )
    ocupacion = tasa_reservaciones(_id)
    calcular_porcentaje_de_tasa(estacionamiento.apertura, estacionamiento.cierre, estacionamiento.capacidad, ocupacion)
    datos_ocupacion = urlencode(ocupacion) # Se convierten los datos del diccionario en el formato key1=value1&key2=value2&...
    return render(
        request,
        'tasa-reservacion.html',
        { "ocupacion" : ocupacion
        , "datos_ocupacion": datos_ocupacion
        }
    )

def grafica_tasa_de_reservacion(request):
    
    # Recuperacion del diccionario para crear el grafico
    try:
        datos_ocupacion = request.GET.dict()
        datos_ocupacion = OrderedDict(sorted((k, float(v)) for k, v in datos_ocupacion.items()))     
        response = HttpResponse(content_type='image/png')
    except:
        return HttpResponse(status=400) # Bad request
    
    # Si el request no viene con algun diccionario
    if (not datos_ocupacion):
        return HttpResponse(status=400) # Bad request
    
    # Configuracion y creacion del grafico de barras con la biblioteca pyplot
    pyplot.switch_backend('Agg') # Para que no use Tk y aparezcan problemas con hilos
    pyplot.bar(range(len(datos_ocupacion)), datos_ocupacion.values(), hold = False, color = '#6495ed')
    pyplot.ylim([0,100])
    pyplot.title('Distribución de los porcentajes por fecha')
    pyplot.xticks(range(len(datos_ocupacion)), list(datos_ocupacion.keys()), rotation=20)
    pyplot.ylabel('Porcentaje (%)')
    pyplot.grid(True, 'major', 'both')
    pyplot.savefig(response, format='png') # Guarda la imagen creada en el HttpResponse creado
    pyplot.close()
    
    return response

# vista para procesar los datos de la billetera
def billetera_all(request):
    billetera = BilleteraElectronica.objects.all()
    
    form = BilleteraForm()
    formAuth = authBilleteraForm()

    # Si es POST, se verifica la información recibida
    if request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        form =BilleteraForm(request.POST)
         
        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
            if len(billetera) == 9999:
                return render(
                        request, 'template-mensaje.html',
                        {'color' : 'red'
                         , 'mensaje' : 'No se pueden crear mas billeteras'
                         }
                    )
                    
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
                        return render(
                            request, 'datos-billetera.html',
                            {'color' : 'green'
                             ,'billetera': obj
                             , 'mensaje' : 'Billetera Creada Satisfactoriamente'
                             }
                        )
                except (IntegrityError):
                    pass
                

    return render(
        request,
        'crear-billetera.html', 
        { 'form': form
         ,'formAuth': formAuth
        }
    )
   
# vista para mostar los datos de la billetera
def billetera_datos(request):
    form = BilleteraForm()
    formAuth = authBilleteraForm()
    # Si es POST, se verifica la información recibida
    if request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        formAuth = authBilleteraForm(request.POST)
         
        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo

        if formAuth.is_valid():
            billetera_autenticada = billetera_autenticar(int(formAuth.cleaned_data['ID']), formAuth.cleaned_data['Pin'])
            if(billetera_autenticada != None):
                return render(
                    request,
                    'datos-billetera.html', 
                    { 'billetera': billetera_autenticada
                    , 'form': form
                    , 'formAuth': formAuth
                    }
                )
                
            else:
                return render(
                    request, 'template-mensaje.html',
                    {'color' : 'red'
                    , 'mensaje' : 'Autenticacion Denegada'
                    }
                )
        

    return render(
                request,
                'crear-billetera.html', 
                { 'form': form
                 ,'formAuth': formAuth
                }
            )
    
# vista para mostar los datos de la billetera
def billetera_recarga(request, _id):
    _id = int(_id)
    try:
        billeteraE = BilleteraElectronica.objects.get(pk = _id)
    except ObjectDoesNotExist:
        raise Http404
    
    form = BilleteraPagoForm()
    
    # Si es POST, se verifica la información recibida
    if request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        form = BilleteraPagoForm(request.POST)
             
        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
            if (form.cleaned_data["monto"] <= Decimal(0.00)):
                return render(
                    request,
                    'mensaje.html',
                    {'color' : 'red'
                    , 'mensaje' : 'Monto debe ser mayor que 0.00'
                    }
                )
                
            elif (not billeteraE.validar_recarga(form.cleaned_data["monto"])):
                return render(
                    request,
                    'mensaje.html',
                    {'color' : 'red'
                    , 'mensaje' : 'Monto de la recarga excede saldo máximo permitido'
                    }
                )
                
            else:
                recarga = Recargas(
                        id = asigna_id_unico(),
                        cedulaTipo = form.cleaned_data['cedulaTipo'],
                        cedula = form.cleaned_data['cedula'],
                        tarjetaTipo = form.cleaned_data['tarjetaTipo'],
                        monto = form.cleaned_data['monto'],
                        fechaTransaccion = datetime.now(),
                        billetera = billeteraE   
                    )
                
                recarga.save()
                billeteraE.recargar_saldo(form.cleaned_data['monto'])
                return render(
                    request, 
                    'recarga-billetera.html',
                    { "id"      : _id
                    , "recarga"    : recarga
                    , "color"   : "green"
                    , "mensaje" : "Se realizo la recarga de la billetera satisfactoriamente"
                    }
                    
                )
        
    return render(
        request,
        'recarga-billetera.html', 
        { 'form': form
        }
    )
    
def validar_reserva(request):
    form = CancelaReservaForm()
    
    if request.method == 'POST':
        form = CancelaReservaForm(request.POST)
        
        
        if form.is_valid():
            pago = pago_autenticar(int(form.cleaned_data['ID']), form.cleaned_data['cedulaTipo'], form.cleaned_data['cedula'])
            if (pago != None):
                if (pago.cancelado):
                    return render(
                        request,
                        'mensaje.html',
                        { 'color': 'red'
                        , 'mensaje' : 'Esta reservacion ya ha sido cancelada'
                        }
                    )
                
                elif (not pago.validar_cancelacion(datetime.now() + timedelta(seconds = 60))):
                    return render(
                        request,
                        'mensaje.html',
                        { 'color': 'red'
                        , 'mensaje': 'Cancelacion denegada, las cancelaciones deben hacerse al menos un minuto antes de que empiece la reservacion' 
                        }          
                    )
                    
                elif (pago.monto <= 0):
                    return render(
                        request,
                        'mensaje.html',
                        { 'color': 'red'
                        , 'mensaje': 'Cancelacion denegada, el monto de la cancelacion debe ser mayor a cero ' 
                        }          
                    )
                    
                else:
                    direccion = "/estacionamientos/" + str(form.cleaned_data['ID']) + "/validar_billetera"
                    return HttpResponseRedirect(direccion)
            
            else:
                return render(
                    request,
                    'mensaje.html',
                    { 'color': 'red'
                    , 'mensaje' : 'ID no existe o CI no corresponde al registrado en el recibo de pago'
                    }
                )
                
    return render(
        request,
        'validar_reserva.html',
         { "form" : form 
          }
    )
    
def validar_billetera(request, id_pago):
    id_pago = int(id_pago)
    
    try:
        pago = Pago.objects.get(pk = id_pago)
    except ObjectDoesNotExist:
        raise Http404
    
    form = authBilleteraForm()
    
    if request.method == 'POST':
        form = authBilleteraForm(request.POST)
        if form.is_valid():
            billetera = billetera_autenticar(int(form.cleaned_data['ID']), form.cleaned_data['Pin'])
            if (billetera != None):
                if(billetera.validar_recarga(pago.monto)):
                    direccion = "/estacionamientos/" + str(pago.id) + "/" + str(billetera.id) + "/cancelar_reserva"
                    return HttpResponseRedirect(direccion)
                    
                else:
                    return render(
                        request,
                        'mensaje.html',
                        { 'color' : 'red'
                        , 'mensaje' : 'Monto de la recarga excede saldo máximo permitido'
                        , 'mensaje2' : '1) Presione volver e ingrese una billetera diferente'
                        , 'mensaje3' : '2) Cree una nueva billetera'
                        }
                    )
                    
            else:
                return render(
                        request,
                        'mensaje.html',
                        { 'color' : 'red'
                        , 'mensaje' : 'Autenticacion Denegada'
                        }
                    )
                
    return render(
        request,
        'validar_billetera.html',
        {'form' : form
        }
    )         
    
def cancelar_reserva(request, id_pago, id_billetera):
    try:
        pago = Pago.objects.get(pk = id_pago)
        billeteraE = BilleteraElectronica.objects.get(pk = id_billetera)
    except ObjectDoesNotExist:
        raise Http404
    
    
    if request.method == 'POST':
        if (pago.validar_cancelacion(datetime.now()) and billeteraE.validar_recarga(pago.monto)):
            cancelacion = Cancelaciones(
                            id = asigna_id_unico(),
                            pagoCancelado = pago,
                            billetera = billeteraE,
                            monto = pago.monto,
                            fechaTransaccion = datetime.now()
            )
            cancelacion.save()
            billeteraE.recargar_saldo(pago.monto)
            pago.cancelar_reserva()
            return render(
                request, 
                'cancelar_reserva.html',
                { 'pago' : pago
                , 'billetera' : billeteraE
                , 'cancelacion' : cancelacion
                , 'color' : 'green'
                , 'mensaje2': 'Reservacion cancelada satisfactoriamente'
                }
            )
            
        else:
            if (not pago.validar_cancelacion(datetime.now())):
                return render(
                        request,
                        'mensaje.html',
                        { 'color': 'red'
                        , 'mensajeFinal': 'Cancelacion denegada, la reserva ya ha empezado' 
                        }          
                )
                
            else:
                return render(
                        request,
                        'mensaje.html',
                        { 'color': 'red'
                        , 'mensajeFinal': 'Cancelacion denegada, la recarga no puede llevarse a cabo' 
                        }          
                )
            
    else:
        return render(
            request, 
            'cancelar_reserva.html',
            { 'pago' : pago
            , 'billetera' : billeteraE
            , 'color' : 'red'
            , 'mensaje1': '¿Desea cancelar esta reservacion?'
            }
        )
