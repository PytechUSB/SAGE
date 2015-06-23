# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
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
    validarHorarioReservaMover,
    marzullo,
    calcularMonto,
    get_client_ip,
    tasa_reservaciones,
    calcular_porcentaje_de_tasa,
    consultar_ingresos,
    billetera_autenticar,
    pago_autenticar,
    asigna_id_unico,
    buscar_historial_billetera
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
    CancelaReservaForm,
    MoverReservaForm,
    PuestosForm, 
    TarifasForm,
    AdministrarSAGEForm,
    cambioPinBilleteraForm
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
    Cancelaciones,
    AdministracionSage
, PagoOperacionesEspeciales)

# Creacion de la unica instancia de la Administracion de SAGE
AdministracionSage.objects.create_AdministracionSage()

MAXPROPIETARIOS=6
MAXESTACIONAMIENTOS=5

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

        # Maximos propietarios:6
        if len(propietarios) >= MAXPROPIETARIOS:
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
                nombres   = form.cleaned_data['nombres'],
                apellidos = form.cleaned_data['apellidos'],
                cedula    = form.cleaned_data['cedula'],
                telefono1 = form.cleaned_data['telefono_1'],
                cedulaTipo= form.cleaned_data['cedulaTipo']
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
        propietario1 = Propietario.objects.get(id=_id)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'GET':
        form_data = {
            'nombres'   : propietario1.nombres,
            'apellidos' : propietario1.apellidos,
            'cedula'    : propietario1.cedula,
            'telefono1' : propietario1.telefono1, 
            'cedulaTipo': propietario1.cedulaTipo
        }
        form = PropietarioForm(data=form_data)

    elif request.method == 'POST':
        # Leemos el formulario
        form = PropietarioForm(request.POST)
        # Si el formulario es valido
        if form.is_valid():
            try:
                Propietario.objects.filter(id=_id).update(
                nombres     = form.cleaned_data['nombres'],
                apellidos   = form.cleaned_data['apellidos'],
                cedula      = form.cleaned_data['cedula'],
                telefono1   = form.cleaned_data['telefono_1'],
                cedulaTipo  =form.cleaned_data['cedulaTipo']
            )
            except:
                return render(
                    request, 'template-mensaje.html',
                    { 'color'   : 'red'
                    , 'mensaje' : 'CÃ©dula ya existente'
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

        # Maximo de estacionamientos
        if len(estacionamientos) >= MAXESTACIONAMIENTOS:
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
                nombre    = form.cleaned_data['nombre'],
                direccion = form.cleaned_data['direccion'],
                rif       = form.cleaned_data['rif'],
                telefono1 = form.cleaned_data['telefono_1'],
                telefono2 = form.cleaned_data['telefono_2'],
                telefono3 = form.cleaned_data['telefono_3'],
                email1    = form.cleaned_data['email_1'],
                email2    = form.cleaned_data['email_2'],
                propietario = form.cleaned_data['propietario']
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
    
    form = EstacionamientoExtendedForm()
    form_data_puestos={
            'particulares'  : estacionamiento.capacidad,
            'camiones'      : estacionamiento.capacidad_C,
            'motos'         : estacionamiento.capacidad_M,
            'discapacitados': estacionamiento.capacidad_D
            }
    formPuestos = PuestosForm(data=form_data_puestos)
    
    if estacionamiento.tarifa:
        form_data = {
            'horarioin'  : estacionamiento.apertura,
            'horarioout' : estacionamiento.cierre,
            'inicioTarifa2' : estacionamiento.tarifa.inicioEspecial,
            'finTarifa2' : estacionamiento.tarifa.finEspecial,
            'esquema'    : estacionamiento.tarifa.__class__.__name__,
            'feriados'   : estacionamiento.feriados,
            'horizonte'   : estacionamiento.horizonte
        }
        if estacionamiento.tarifaFeriados:
            form_data.update({
                'inicioTarifaFeriados2' : estacionamiento.tarifaFeriados.inicioEspecial,
                'finTarifaFeriados2' : estacionamiento.tarifaFeriados.finEspecial,
                'esquemaFeriados'    : estacionamiento.tarifaFeriados.__class__.__name__,
                'aceptaFeriados'    : True
            })
            
            
        form = EstacionamientoExtendedForm(data=form_data)

    if request.method == 'POST' and 'botonSubmit' in request.POST:
        # Leemos el formulario
        form = EstacionamientoExtendedForm(request.POST)
        # Si el formulario
        if form.is_valid():
            horaIn  = form.cleaned_data['horarioin']
            horaOut = form.cleaned_data['horarioout']
            tipo    = form.cleaned_data['esquema']
            inicioTarifa2        = form.cleaned_data['inicioTarifa2']
            finTarifa2           = form.cleaned_data['finTarifa2']
            horizonte            = request.POST['horizonte']
            aceptaFeriados       = form.cleaned_data['aceptaFeriados']
            feriados             = form.cleaned_data['feriados']
            tipo2                = form.cleaned_data['esquemaFeriados']
            inicioTarifaFeriados = form.cleaned_data['inicioTarifaFeriados']
            finTarifaFeriados    = form.cleaned_data['finTarifaFeriados']
            
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
            #Verificamos si el esquema existe, de ser asi copiamos todos sus datos
            if (estacionamiento.tarifa):
                esquemaTarifa = eval(tipo)(
                    tarifa      = estacionamiento.tarifa.tarifa,
                    tarifa2      = estacionamiento.tarifa.tarifa2,
                    tarifa_M      = estacionamiento.tarifa.tarifa_M,
                    tarifa2_M      = estacionamiento.tarifa.tarifa2_M,
                    tarifa_C      = estacionamiento.tarifa.tarifa_C,
                    tarifa2_C      = estacionamiento.tarifa.tarifa2_C,
                    tarifa_D      = estacionamiento.tarifa.tarifa_D,
                    tarifa2_D      = estacionamiento.tarifa.tarifa2_D,
                    inicioEspecial  = inicioTarifa2,
                    finEspecial     = finTarifa2
                )
                #Borramos el esquema anterior
                estacionamiento.tarifa.delete()
            else:
                esquemaTarifa = eval(tipo)(
                    tarifa      = 0,
                    inicioEspecial  = inicioTarifa2,
                    finEspecial     = finTarifa2
                )
            if (aceptaFeriados):
                if (estacionamiento.tarifaFeriados):
                    esquemaTarifaFeriados = eval(tipo2)(
                        tarifa      = estacionamiento.tarifaFeriados.tarifa,
                        tarifa2      = estacionamiento.tarifaFeriados.tarifa2,
                        tarifa_M      = estacionamiento.tarifaFeriados.tarifa_M,
                        tarifa2_M      = estacionamiento.tarifaFeriados.tarifa2_M,
                        tarifa_C      = estacionamiento.tarifaFeriados.tarifa_C,
                        tarifa2_C      = estacionamiento.tarifaFeriados.tarifa2_C,
                        tarifa_D      = estacionamiento.tarifaFeriados.tarifa_D,
                        tarifa2_D      = estacionamiento.tarifaFeriados.tarifa2_D,
                        inicioEspecial = inicioTarifaFeriados,
                        finEspecial    = finTarifaFeriados
                    )
                    #Borramos el esquema anterior
                    estacionamiento.tarifaFeriados.delete()
                else:    
                    esquemaTarifaFeriados = eval(tipo2)(
                        tarifa      = 0,
                        inicioEspecial = inicioTarifaFeriados,
                        finEspecial    = finTarifaFeriados
                    )
                esquemaTarifaFeriados.save()
                estacionamiento.tarifaFeriados = esquemaTarifaFeriados
            else:
                if (estacionamiento.tarifaFeriados is not None):
                    estacionamiento.tarifaFeriados.delete()
            esquemaTarifa.save()
            
            estacionamiento.feriados = feriados
            estacionamiento.horizonte = horizonte
            estacionamiento.tarifa   = esquemaTarifa
            estacionamiento.apertura = horaIn
            estacionamiento.cierre   = horaOut
            estacionamiento.save()
            
    elif request.method == 'POST' and 'botonPuestos' in request.POST:
        form_data_puestos={
                'particulares' : request.POST['particulares'],
                'camiones'     : request.POST['camiones'],
                'motos'        : request.POST['motos'],
                'discapacitados' : request.POST['discapacitados']
            }
        formPuestos=PuestosForm(data=form_data_puestos)
        
        if formPuestos.is_valid():
            estacionamiento.capacidad = request.POST['particulares']
            estacionamiento.capacidad_C = request.POST['camiones']
            estacionamiento.capacidad_M = request.POST['motos']
            estacionamiento.capacidad_D = request.POST['discapacitados']
            estacionamiento.save()
        else:    
            try:
                # '__all__' expone el error definido en el clean de PuestosForm
                formPuestos.errors['__all__']
                mensaje='Debe haber al menos un puesto.'
            except:
                mensaje='Todos los campos son obligatorios'
            return render(
                request,
                'detalle-estacionamiento.html',
                { 'form': form
                , 'formPuestos': formPuestos
                , 'estacionamiento': estacionamiento
                , 'errorDialog' : mensaje
                }
            )
    estacionamiento = Estacionamiento.objects.get(id=_id) 
    try:
        # '__all__' expone el error definido en el clean de EstacionamientoExtendedForm
        form.errors['__all__']
    except:
        pass

    return render(
        request,
        'detalle-estacionamiento.html',
        { 'form': form
        , 'formPuestos': formPuestos
        , 'estacionamiento': estacionamiento
        }
    )

def estacionamiento_tarifa_especial(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacionamiento = Estacionamiento.objects.get(id=_id)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == 'GET':
        mensaje=""
        #Extraemos la data de cada forma desde los esquemas tarifarios de estacionamiento
        form_data = {
            'Particulares_tarifa'   : estacionamiento.tarifa.tarifa,
            'Particulares_tarifa2' : estacionamiento.tarifa.tarifa2
        }
        formParticulares=TarifasForm(data=form_data,prefix='Particulares')
        
        form_data = {
            'Motos_tarifa'   : estacionamiento.tarifa.tarifa_M,
            'Motos_tarifa2' : estacionamiento.tarifa.tarifa2_M
        }
        formMotos=TarifasForm(data=form_data,prefix='Motos')
        
        form_data = {
            'Camiones_tarifa'   : estacionamiento.tarifa.tarifa_C,
            'Camiones_tarifa2' : estacionamiento.tarifa.tarifa2_C
        }
        formCamiones=TarifasForm(data=form_data,prefix='Camiones')
        
        form_data = {
            'Discapacitados_tarifa'   : estacionamiento.tarifa.tarifa_D,
            'Discapacitados_tarifa2' : estacionamiento.tarifa.tarifa2_D
        }
        formDisc=TarifasForm(data=form_data,prefix='Discapacitados')
        
        if estacionamiento.tarifaFeriados:
            form_data = {
                'FeriadosParticulares_tarifa'   : estacionamiento.tarifaFeriados.tarifa,
                'FeriadosParticulares_tarifa2' : estacionamiento.tarifaFeriados.tarifa2
            }
            formFeriadosParticulares = TarifasForm(data=form_data,prefix='FeriadosParticulares')
            form_data = {
                'FeriadosDiscapacitados_tarifa'   : estacionamiento.tarifaFeriados.tarifa_D,
                'FeriadosDiscapacitados_tarifa2' : estacionamiento.tarifaFeriados.tarifa2_D
            }
            formFeriadosDisc=TarifasForm(data=form_data,prefix='FeriadosDiscapacitados')
            form_data = {
                'FeriadosCamiones_tarifa'   : estacionamiento.tarifaFeriados.tarifa_C,
                'FeriadosCamiones_tarifa2' : estacionamiento.tarifaFeriados.tarifa2_C
            }
            formFeriadosCamiones=TarifasForm(data=form_data,prefix='FeriadosCamiones')
            form_data = {
                'FeriadosMotos_tarifa'   : estacionamiento.tarifaFeriados.tarifa_M,
                'FeriadosMotos_tarifa2' : estacionamiento.tarifaFeriados.tarifa2_M
            }
            formFeriadosMotos=TarifasForm(data=form_data,prefix='FeriadosMotos')
        else:
            formFeriadosParticulares = TarifasForm(prefix='FeriadosParticulares')
            formFeriadosDisc=TarifasForm(prefix='FeriadosDiscapacitados')
            formFeriadosCamiones=TarifasForm(prefix='FeriadosCamiones')
            formFeriadosMotos=TarifasForm(prefix='FeriadosMotos')
            
            
    if request.method == 'POST':
            formParticulares=TarifasForm(request.POST,prefix='Particulares')
            formMotos = TarifasForm(request.POST,prefix='Motos')
            formCamiones=TarifasForm(request.POST,prefix='Camiones')
            formDisc=TarifasForm(request.POST,prefix='Discapacitados')
            formFeriadosParticulares = TarifasForm(request.POST,prefix='FeriadosParticulares')
            formFeriadosMotos = TarifasForm(request.POST,prefix='FeriadosMotos')
            formFeriadosCamiones=TarifasForm(request.POST,prefix='FeriadosCamiones')
            formFeriadosDisc=TarifasForm(request.POST,prefix='FeriadosDiscapacitados')
            mensaje=""
            errorFeriados=False
            
            #Si son válidas extraemos las tarifas regulares y feriadas
            if formMotos.is_valid():
                estacionamiento.tarifa.tarifa_M        = formMotos.cleaned_data['tarifa']
                estacionamiento.tarifa.tarifa2_M       = formMotos.cleaned_data['tarifa2']
            if formParticulares.is_valid():
                estacionamiento.tarifa.tarifa          = formParticulares.cleaned_data['tarifa']
                estacionamiento.tarifa.tarifa2         = formParticulares.cleaned_data['tarifa2']
            if formCamiones.is_valid():
                estacionamiento.tarifa.tarifa_C        = formCamiones.cleaned_data['tarifa']
                estacionamiento.tarifa.tarifa2_C       = formCamiones.cleaned_data['tarifa2']
            if formDisc.is_valid():
                estacionamiento.tarifa.tarifa_D        = formDisc.cleaned_data['tarifa']
                estacionamiento.tarifa.tarifa2_D       = formDisc.cleaned_data['tarifa2']
            
            if estacionamiento.tarifaFeriados:
                if formFeriadosParticulares.is_valid():
                    estacionamiento.tarifaFeriados.tarifa          = formFeriadosParticulares.cleaned_data['tarifa']
                    estacionamiento.tarifaFeriados.tarifa2         = formFeriadosParticulares.cleaned_data['tarifa2']
                if formFeriadosMotos.is_valid():
                    estacionamiento.tarifaFeriados.tarifa_M         = formFeriadosMotos.cleaned_data['tarifa']
                    estacionamiento.tarifaFeriados.tarifa2_M        = formFeriadosMotos.cleaned_data['tarifa2']
                if formFeriadosCamiones.is_valid():
                    estacionamiento.tarifaFeriados.tarifa_C        = formFeriadosCamiones.cleaned_data['tarifa']
                    estacionamiento.tarifaFeriados.tarifa2_C       = formFeriadosCamiones.cleaned_data['tarifa2']
                if formFeriadosDisc.is_valid():
                    estacionamiento.tarifaFeriados.tarifa_D        = formFeriadosDisc.cleaned_data['tarifa']
                    estacionamiento.tarifaFeriados.tarifa2_D       = formFeriadosDisc.cleaned_data['tarifa2']
                if ((formFeriadosParticulares.errors and estacionamiento.capacidad)     or 
                        (formFeriadosCamiones.errors and estacionamiento.capacidad_C)   or 
                        (formFeriadosMotos.errors and estacionamiento.capacidad_M)      or
                        (formFeriadosDisc.errors and estacionamiento.capacidad_D)): 
                    errorFeriados=True
                else: estacionamiento.tarifaFeriados.save() #Solo si no hay error guardamos los datos
            print(formParticulares.errors)
            # De morgan poderoso
            if not(errorFeriados or ((formParticulares.errors and estacionamiento.capacidad) 
                                        or (formCamiones.errors and estacionamiento.capacidad_C)
                                        or (formMotos.errors and estacionamiento.capacidad_M)
                                        or (formDisc.errors and estacionamiento.capacidad_D))): 
                mensaje="Se han cambiado las tarifas exitosamente"
                estacionamiento.tarifa.save()
                estacionamiento.save() #Solo si no hay error guardamos los datos
            
    return render(
                    request,
                    'tarifas-especiales.html',
                    { 'estacionamiento'         : estacionamiento
                    , 'formParticulares'        : formParticulares
                    , 'formCamiones'            : formCamiones
                    , 'formMotos'               : formMotos
                    , 'formDisc'                : formDisc
                    , 'formFeriadosCamiones'    : formFeriadosCamiones
                    , 'formFeriadosParticulares': formFeriadosParticulares
                    , 'formFeriadosMotos'       : formFeriadosMotos
                    , 'formFeriadosDisc'        : formFeriadosDisc
                    , 'ocultarParametros'       : True
                    , 'mensaje'                 : mensaje
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
            cedulaTipo = form.cleaned_data['cedulaTipo']
            try:
                propietario = Propietario.objects.get(cedula=cedula, cedulaTipo=cedulaTipo)
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
            vehiculoTipo  = form.cleaned_data['vehiculoTipo']
            inicioReserva = form.cleaned_data['inicio']
            finalReserva  = form.cleaned_data['final']

            # debería funcionar con excepciones, y el mensaje debe ser mostrado
            # en el mismo formulario
            m_validado = validarHorarioReserva(
                inicioReserva,
                finalReserva,
                estacionamiento.apertura,
                estacionamiento.cierre,
                estacionamiento.horizonte,
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

            if marzullo(_id, inicioReserva, finalReserva, vehiculoTipo):
                reservaFinal = Reserva(
                    estacionamiento = estacionamiento,
                    inicioReserva   = inicioReserva,
                    finalReserva    = finalReserva,
                    vehiculoTipo    = vehiculoTipo,
                )

                #calcula el monto a pagar
                monto = Decimal(calcularMonto(estacionamiento.id, inicioReserva, finalReserva, vehiculoTipo))
                request.session['monto'] = float(monto)
                                
                request.session['vehiculoTipo']        = vehiculoTipo
                request.session['finalReservaHora']    = finalReserva.hour
                request.session['finalReservaMinuto']  = finalReserva.minute
                request.session['inicioReservaHora']   = inicioReserva.hour
                request.session['inicioReservaMinuto'] = inicioReserva.minute
                request.session['anioinicial']  = inicioReserva.year
                request.session['mesinicial']   = inicioReserva.month
                request.session['diainicial']   = inicioReserva.day
                request.session['aniofinal']    = finalReserva.year
                request.session['mesfinal']     = finalReserva.month
                request.session['diafinal']     = finalReserva.day
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
                return render(
                    request,
                    'template-mensaje.html',
                    {'color'   : 'red'
                    , 'mensaje' : 'No hay un puesto disponible para Vehiculo ' + str(vehiculoTipo) + 
                                  ' en ese horario'
                    }
                )

    return render(
        request,
        'reserva.html',
        { 'form': form
        , 'estacionamiento': estacionamiento
        }
    )

def pago_reserva_aux(request, monto, estacionamiento, form = None, idFacturaReservaMovida = None):
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
        vehiculoTipo    = request.session['vehiculoTipo'],
    )

    # Se guarda la reserva en la base de datos
    reservaFinal.save()
    
    if form != None and form.cleaned_data['ID'] == '':
        form.cleaned_data['ID'] = None
        
    if (idFacturaReservaMovida == None):
        pago = Pago(
            id = asigna_id_unico(),
            fechaTransaccion = datetime.now(),
            cedula           = form.cleaned_data['cedula'],
            cedulaTipo       = form.cleaned_data['cedulaTipo'],
            monto            = monto,
            tarjetaTipo      = form.cleaned_data['tarjetaTipo'],
            reserva          = reservaFinal,
            idBilletera      = form.cleaned_data['ID'],
            nombreUsuario    = form.cleaned_data['nombre'],
            apellidoUsuario  = form.cleaned_data['apellido']
        )
        
    else:
        pagoAnterior = Pago.objects.get(pk = idFacturaReservaMovida)
        if monto <= pagoAnterior.monto and form == None:
            pago = Pago(
                id = asigna_id_unico(),
                fechaTransaccion = datetime.now(),
                cedula           = pagoAnterior.cedula,
                cedulaTipo       = pagoAnterior.cedulaTipo,
                monto            = monto,
                tarjetaTipo      = pagoAnterior.tarjetaTipo,
                reserva          = reservaFinal,
                facturaMovida    = pagoAnterior,
                idBilletera      = pagoAnterior.idBilletera,
                nombreUsuario    = pagoAnterior.nombreUsuario,
                apellidoUsuario  = pagoAnterior.apellidoUsuario
            )
            
        else:
            pago = Pago(
                id = asigna_id_unico(),
                fechaTransaccion = datetime.now(),
                cedula           = pagoAnterior.cedula,
                cedulaTipo       = pagoAnterior.cedulaTipo,
                monto            = monto,
                tarjetaTipo      = form.cleaned_data['tarjetaTipo'],
                reserva          = reservaFinal,
                facturaMovida    = pagoAnterior,
                idBilletera      = form.cleaned_data['ID'],
                nombreUsuario    = form.cleaned_data['nombre'],
                apellidoUsuario  = form.cleaned_data['apellido']
            )
             
    return pago


def estacionamiento_pago(request, _id):
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
                        pago = pago_reserva_aux(
                            request, 
                            monto, 
                            estacionamiento,
                            form
                        )
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
                pago = pago_reserva_aux(
                            request,
                            monto, 
                            estacionamiento,
                            form
                )
                
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
            cedulaTipo    = form.cleaned_data['cedulaTipo']
            facturas      = Pago.objects.filter(cedula = cedula)
            facturas      = facturas.filter(cedulaTipo = cedulaTipo)
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
        estacionamiento.horizonte,
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
    capacidad_total = estacionamiento.capacidadTotal()
    calcular_porcentaje_de_tasa(estacionamiento.apertura, estacionamiento.cierre, capacidad_total, ocupacion)
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
                historial = buscar_historial_billetera(int(formAuth.cleaned_data['ID']))
                return render(
                    request,
                    'datos-billetera.html', 
                    { 'billetera': billetera_autenticada
                    , 'historial' : historial
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
                        billetera = billeteraE,
                        numTarjeta  = form.cleaned_data['tarjeta']
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
    
def validar_reserva(request, link = ''):
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
                        , 'mensaje': 'Cancelacion denegada, las operaciones cancelar o mover reserva deben hacerse al menos un minuto antes de que empiece la reservacion' 
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
                    direccion = "/estacionamientos/" + str(form.cleaned_data['ID']) + "/" + link
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
    
def validar_billetera(request, id_pago, link = ''):
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
                    direccion = "/estacionamientos/" + str(pago.id) + "/" + str(billetera.id) + "/" + link
                    return HttpResponseRedirect(direccion)
                    
                else:
                    return render(
                        request,
                        'mensaje.html',
                        { 'color' : 'red'
                        , 'mensaje' : 'Monto de la recarga excede saldo máximo permitido'
                        , 'mensaje2' : '1) Presione volver e ingrese una billetera diferente'
                        , 'mensaje3' : '2) Cree una nueva billetera e intentelo de nuevo'
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
    id_pago = int(id_pago)
    id_billetera = int(id_billetera)
    
    try:
        pago = Pago.objects.get(pk = id_pago)
        billeteraE = BilleteraElectronica.objects.get(pk = id_billetera)
    except ObjectDoesNotExist:
        raise Http404
    
    administracion = AdministracionSage.objects.get(pk = 1)
    aplicaCargo = pago.factura_inicial_pagada_billetera()
    if (aplicaCargo):
        monto_debitar = administracion.calcular_monto(pago.monto)
    else:
        monto_debitar = 0
    
    monto_reembolso = pago.monto - monto_debitar
    
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
            if (aplicaCargo):
                pago_op_especial = PagoOperacionesEspeciales(
                                    id = asigna_id_unico(),
                                    monto = monto_debitar,
                                    billetera = billeteraE,
                                    cancelacion = cancelacion,
                                    fechaTransaccion = datetime.now()
                )
                pago_op_especial.save()
                
            billeteraE.recargar_saldo(monto_reembolso)
            pago.cancelar_reserva()
            return render(
                request, 
                'cancelar_reserva.html',
                { 'pago' : pago
                , 'billetera' : billeteraE
                , 'monto_debitar': monto_debitar
                , 'monto_reembolso' : monto_reembolso
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
            , 'monto_debitar': monto_debitar
            , 'monto_reembolso' : monto_reembolso
            , 'color' : 'red'
            , 'mensaje1': '¿Desea cancelar esta reservacion?'
            }
        )

def mover_reserva(request, id_pago):
    id_pago = int(id_pago)
    
    try:
        pago = Pago.objects.get(pk = id_pago)
        estacionamiento = pago.reserva.estacionamiento
        
    except:
        raise Http404
    
    form = MoverReservaForm()
    
    if request.method == 'POST':
        form = MoverReservaForm(request.POST)
        if form.is_valid():
            inicioReserva = form.cleaned_data['inicio']
            if inicioReserva < datetime.now():
                return render(
                    request,          
                    'mensaje.html',
                    { 'color' : 'red'
                    , 'mensaje' : 'El inicio de su reserva no puede ser antes de la hora actual' 
                    }
                )
            reserva = pago.reserva 
            variacionTiempo = reserva.finalReserva - reserva.inicioReserva
            finalReserva = inicioReserva + variacionTiempo
            vehiculoTipo = reserva.vehiculoTipo
            horarioValidado = validarHorarioReservaMover(
                inicioReserva, 
                finalReserva, 
                estacionamiento.apertura, 
                estacionamiento.cierre,
                estacionamiento.horizonte
            )
            
            if not horarioValidado[0]:
                return render(
                    request,          
                    'mensaje.html',
                    { 'color' : 'red'
                    , 'mensaje' : horarioValidado[1]  
                    }
                )
            
            if marzullo(estacionamiento.id, inicioReserva, finalReserva, vehiculoTipo, reserva.id):
                reservaFinal = Reserva(
                    estacionamiento = estacionamiento,
                    inicioReserva   = inicioReserva,
                    finalReserva    = finalReserva,
                    vehiculoTipo    = vehiculoTipo,
                )
                
                #calcular monto a pagar
                monto = Decimal(calcularMonto(estacionamiento.id, inicioReserva, finalReserva, vehiculoTipo))
                
                request.session['vehiculoTipo']        = vehiculoTipo
                request.session['finalReservaHora']    = finalReserva.hour
                request.session['finalReservaMinuto']  = finalReserva.minute
                request.session['inicioReservaHora']   = inicioReserva.hour
                request.session['inicioReservaMinuto'] = inicioReserva.minute
                request.session['anioinicial']  = inicioReserva.year
                request.session['mesinicial']   = inicioReserva.month
                request.session['diainicial']   = inicioReserva.day
                request.session['aniofinal']    = finalReserva.year
                request.session['mesfinal']     = finalReserva.month
                request.session['diafinal']     = finalReserva.day
                
                administracion = AdministracionSage.objects.get(pk = 1)
                if pago.tarjetaTipo != 'Billetera Electronica':
                    monto_debitar = administracion.calcular_monto(monto)
                else:
                    if pago.facturaMovida != None:
                        monto_debitar = administracion.calcular_monto(monto)
                    else:
                        monto_debitar = 0
                        
                
                request.session['cargoOperacionesEspeciales'] = float(monto_debitar)
                if (monto + monto_debitar) < pago.monto: 
                    diferenciaMonto = Decimal(pago.monto - monto)
                    request.session['monto'] = float(diferenciaMonto)
                    return render(
                        request,
                        'confirmar-mover.html',
                        { 'id'      : pago.id
                        , 'monto'   : monto
                        , 'monto_debitar' : monto_debitar
                        , 'montoAnterior' : pago.monto
                        , 'diferencia' : diferenciaMonto - monto_debitar
                        , 'reserva' : reservaFinal
                        , 'color'   : 'green'
                        , 'mensaje' : 'Existe un puesto disponible'
                        , 'tituloMonto' : 'Monto a recargar'
                        }
                    )
                        
                else:
                    diferenciaMonto = Decimal(monto - pago.monto)
                    request.session['monto'] = float(diferenciaMonto)
                    return render(
                        request,
                        'confirmar-mover.html',
                        { 'id'      : pago.id
                        , 'monto'   : monto
                        , 'monto_debitar' : monto_debitar
                        , 'montoAnterior' : pago.monto
                        , 'diferencia' : diferenciaMonto + monto_debitar
                        , 'reserva' : reservaFinal
                        , 'color'   : 'green'
                        , 'mensaje' : 'Existe un puesto disponible'
                        , 'tituloMonto' : 'Monto a pagar'
                        }
                    )

            else:
                return render(
                    request,
                    'mensaje.html',
                    {'color'   : 'red'
                    , 'mensaje' : 'No hay un puesto disponible para Vehiculo' + str(pago.reserva.vehiculoTipo) + 
                                  ' en ese horario'
                    }
                )

    return render(
        request,
        'mover-reserva.html',
        { 'form': form
        , 'estacionamiento': estacionamiento
        }
    )
    
def recarga_mover(request, id_pago, id_billetera):
    id_pago = int(id_pago)
    id_billetera = int(id_billetera)
    
    try:
        pago = Pago.objects.get(pk = id_pago)
        billetera = BilleteraElectronica.objects.get(pk = id_billetera)
        
    except:
        raise Http404
    
            
    estacionamiento = pago.reserva.estacionamiento
    montoARecargar = Decimal(request.session['monto']).quantize(Decimal('1.00'))
    monto_debitar = Decimal(request.session['cargoOperacionesEspeciales']).quantize(Decimal('1.00'))
    pago_movido = pago_reserva_aux(request, pago.monto - montoARecargar, estacionamiento, idFacturaReservaMovida = id_pago)
    pago_movido.save()
    cancelacion = Cancelaciones(
        id = asigna_id_unico(),
        pagoCancelado = pago,
        billetera = billetera,
        monto = montoARecargar,
        fechaTransaccion = datetime.now()    
    )
    cancelacion.save()
    
    if ((pago.tarjetaTipo != 'Billetera Electronica') or 
        (pago.tarjetaTipo == 'Billetera Electronica' and pago.facturaMovida != None)):
        pago_op_especial = PagoOperacionesEspeciales(
                        id = asigna_id_unico(),
                        monto = monto_debitar,
                        billetera = billetera,
                        cancelacion = cancelacion,
                        fechaTransaccion = datetime.now()
        )
        pago_op_especial.save()
    
    
    pago.fue_movido()
    billetera.recargar_saldo(montoARecargar - monto_debitar)
    
    
    return render(
        request,
        'pago-mover.html',
        { 'pago'    : pago_movido
        , 'id_billetera' : id_billetera
        , 'id_pago_anterior' : id_pago
        , 'monto' : montoARecargar - monto_debitar
        , 'monto_debitar': monto_debitar
        , 'color'   : 'green'
        , 'mensaje' : 'Se movio la reserva satisfactoriamente.'
        }
    )
    
def pago_mover(request, id_pago):
    idFacturaReservaMovida = int(id_pago)
    
    try:
        pago = Pago.objects.get(pk = idFacturaReservaMovida)
        estacionamiento = pago.reserva.estacionamiento   
    except:
        raise Http404
    
    if (estacionamiento.apertura is None):
        return HttpResponse(status = 403) # No esta permitido acceder a esta vista aun
    
    monto = Decimal(request.session['monto']).quantize(Decimal('1.00'))
    monto_debitar = Decimal(request.session['cargoOperacionesEspeciales']).quantize(Decimal('1.00'))
    
    if ((request.method == 'GET') and (monto + monto_debitar == 0)):
        estacionamiento = pago.reserva.estacionamiento
        pago_movido = pago_reserva_aux(request, pago.monto, estacionamiento, idFacturaReservaMovida = id_pago)
        pago_movido.save()
        cancelacion = Cancelaciones(
            id = asigna_id_unico(),
            pagoCancelado = pago,
            monto = 0,
            fechaTransaccion = datetime.now()    
        )
        cancelacion.save()
        pago.fue_movido()
        
        return render(
            request,
            'pago.html',
            { 'pago'    : pago_movido
            , 'id_pago_anterior' : id_pago
            , 'monto_debitar' : monto_debitar
            , 'monto_total' : pago_movido.monto + monto_debitar
            , 'color'   : 'green'
            , 'mensaje' : 'Se movio la reserva satisfactoriamente.'
            }
        )
        
    
    form = PagoForm()
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
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
                    if(not billeteraE.validar_consumo(monto + monto_debitar)):
                        return render(
                            request, 'mensaje.html',
                            {'color' : 'red'
                            , 'mensaje' : 'Saldo Insuficiente'
                            }
                        ) 
                        
                    else:
                        pago_movido = pago_reserva_aux(request, monto + pago.monto, estacionamiento, form, id_pago)
                        pago_movido.save()
                        cancelacion = Cancelaciones(
                            id = asigna_id_unico(),
                            pagoCancelado = pago,
                            monto = 0,
                            fechaTransaccion = datetime.now()    
                        )
                        cancelacion.save()
                        if ((pago.tarjetaTipo != 'Billetera Electronica') or 
                            (pago.tarjetaTipo == 'Billetera Electronica' and pago.facturaMovida != None)):
                            pago_op_especial = PagoOperacionesEspeciales(
                                            id = asigna_id_unico(),
                                            monto = monto_debitar,
                                            pago_movido = pago_movido,
                                            billetera = billeteraE,
                                            fechaTransaccion = datetime.now()
                            )
                            pago_op_especial.save()
                            
                        pago.fue_movido()
                        estacionamiento = pago.reserva.estacionamiento
                        billeteraE.consumir_saldo(monto + monto_debitar)
                        
                        if (billeteraE.saldo == 0):
                            return render(
                                request,
                                'pago.html',
                                { 'pago'    : pago_movido
                                , 'id_pago_anterior' : id_pago
                                , 'monto_debitar' : monto_debitar
                                , 'monto_total' : pago_movido.monto + monto_debitar 
                                , 'color'   : 'green'
                                , 'mensaje' : 'Se movio la reserva satisfactoriamente.'
                                , 'color2'  : 'red'
                                , 'mensaje2': 'Se recomienda recargar la billetera.'
                                }
                            )
                            
                        else:
                            return render(
                                request,
                                'pago.html',
                                { 'pago'    : pago_movido
                                , 'id_pago_anterior' : id_pago
                                , 'monto_debitar' : monto_debitar
                                , 'monto_total' : pago_movido.monto + monto_debitar 
                                , 'color'   : 'green'
                                , 'mensaje' : 'Se movio la reserva satisfactoriamente.'
                                }
                            )
                        
            
            
            else:
                estacionamiento = pago.reserva.estacionamiento
                pago_movido = pago_reserva_aux(request, monto + pago.monto, estacionamiento, form, id_pago)
                pago_movido.save()
                cancelacion = Cancelaciones(
                    id = asigna_id_unico(),
                    pagoCancelado = pago,
                    monto = 0,
                    fechaTransaccion = datetime.now()    
                )
                cancelacion.save()
                if ((pago.tarjetaTipo != 'Billetera Electronica') or 
                            (pago.tarjetaTipo == 'Billetera Electronica' and pago.facturaMovida != None)):
                            pago_op_especial = PagoOperacionesEspeciales(
                                            id = asigna_id_unico(),
                                            monto = monto_debitar,
                                            pago_movido = pago_movido,
                                            fechaTransaccion = datetime.now()
                            )
                            pago_op_especial.save()
                pago.fue_movido()
                
                return render(
                    request,
                    'pago.html',
                    { 'pago'    : pago_movido
                    , 'id_pago_anterior' : id_pago
                    , 'monto_debitar' : monto_debitar
                    , 'monto_total' : pago_movido.monto + monto_debitar 
                    , 'color'   : 'green'
                    , 'mensaje' : 'Se movio la reserva satisfactoriamente.'
                    }
                )

    return render(
        request,
        'pago.html',
        { 'form' : form }
    )
    
def administrar_sage(request):
    administracion = AdministracionSage.objects.get(pk = 1)
    form = AdministrarSAGEForm()
    if request.method == 'POST':
        # Creamos un formulario con los datos que recibimos
        form = AdministrarSAGEForm(request.POST)
         
        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
            porcentaje = form.cleaned_data['porcentaje']
            if (porcentaje > Decimal('9.9')) or (porcentaje < 0):
                return render(
                    request, 
                    'template-mensaje.html',
                    { 'mensaje' : 'El porcentaje debe ser un número decimal entre 0 y 9.9'
                    , 'color' : 'red' 
                    }
                )
                
            else: 
                administracion.cambiar_porcentaje(porcentaje)
                return render(
                    request, 
                    'mensaje_cambio_porcentaje.html',
                    { 'mensaje' : 'Porcentaje cambiado satisfactoriamente'
                    , 'color' : 'green' 
                    }
                )
            
    return render(
        request,
        'administrar_sage.html',
        { 'porcentaje' : administracion.porcentaje
        , 'form' : form 
        }
    )
    
def cambio_pin(request, _id):
    _id = int(_id)
    try:
        billeteraE = BilleteraElectronica.objects.get(pk = _id)
    except ObjectDoesNotExist:
        raise Http404
    
    form = cambioPinBilleteraForm()
    
    # Si es POST, se verifica la información recibida
    if request.method == 'POST':

        try:
            billeteraE = BilleteraElectronica.objects.get(pk = _id)
        except ObjectDoesNotExist:
            raise Http404
        
        form = cambioPinBilleteraForm(request.POST)
             
        # Si el formulario es valido, entonces creamos un objeto con
        # el constructor del modelo
        if form.is_valid():
            pines_validados = billeteraE.validar_cambio_pin(
                form.cleaned_data["Pin"],
                form.cleaned_data["nuevo_Pin1"],
                form.cleaned_data["nuevo_Pin2"]
            )
            if (not pines_validados[0]):
                return render(
                    request,
                    'mensaje.html',
                    {'color' : 'red'
                    , 'mensajeFinal' : pines_validados[1]
                    }
                )
                
            else:
                billeteraE.cambiar_pin(
                    form.cleaned_data["Pin"],
                    form.cleaned_data["nuevo_Pin1"],
                    form.cleaned_data["nuevo_Pin2"]
                )
                return render(
                    request,
                    'mensaje.html',
                    {'color' : 'green'
                    , 'mensajeFinal' : 'Cambio de PIN realizado satisfactoriamente'
                    }
                )
                           
    return render(
        request,
        'cambio_pin.html', 
        { 'form': form,
          'billetera': billeteraE  
        }
    )
