# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator
from django.forms.widgets import SplitDateTimeWidget
from estacionamientos.models import Propietario
from decimal import Decimal

# Límites para los campos  
MAXNOMBRE=100
MAXRIF=11
MAXCEDULA=10
MAXTELEFONO=11
MAXMAIL=30
MAXTARJETA=16
MAXPIN=4
MAXID=4
MAXMONTO=7
MAXDECIMALS = 2
SMAX = 10000

class CustomSplitDateTimeWidget(SplitDateTimeWidget):

    def format_output(self, rendered_widgets):
        return '<p></p>'.join(rendered_widgets)


class EstacionamientoForm(forms.Form):
    name_validator = RegexValidator(
        regex   = '^[0-9¡!¿?\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][0-9¡!¿?\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
        message = 'La entrada debe ser un nombre en Español sin símbolos especiales.'
    )
    
    rif_validator = RegexValidator(
        regex   = '^[JVD]-\d{8}-?\d$',
        message = 'Introduzca un RIF con un formato válido de la forma X-xxxxxxxxx.'
    )
    
    phone_validator = RegexValidator(
        regex   = '^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-?\d{7}',
        message = 'Debe introducir un formato válido de teléfono.'
    )
    
    propietario = forms.ModelChoiceField(
        Propietario.objects.all(),
        required = True,
        empty_label    = "Introduzca Propietario"
    )
    
    nombre = forms.CharField(
        required = True,
        max_length=MAXNOMBRE,
        label    = "Nombre del Estacionamiento",
        validators = [name_validator],
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Nombre del Estacionamiento *'
            , 'pattern'     : name_validator.regex.pattern
            , 'message'     : name_validator.message
            }
        )
    )

    direccion = forms.CharField(
        required = True,
        max_length=MAXNOMBRE,
        label    = "Direccion",
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Dirección *'
            , 'message'     : 'La entrada no puede quedar vacía.'
            }
        )
    )
    
    rif = forms.CharField(
        required   = True,
        label      = "RIF",
        max_length=MAXRIF,
        validators = [rif_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'RIF: X-xxxxxxxxx *'
            , 'pattern'     : rif_validator.regex.pattern
            , 'message'     : rif_validator.message
            }
        )
    )
    
    telefono_1 = forms.CharField(
        required   = False,
        max_length=MAXTELEFONO,
        validators = [phone_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Teléfono 1'
            , 'pattern'     : phone_validator.regex.pattern
            , 'message'     : phone_validator.message
            }
        )
    )

    telefono_2 = forms.CharField(
        required   = False,
        max_length=MAXTELEFONO,
        validators = [phone_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Teléfono 2'
            , 'pattern'     : phone_validator.regex.pattern
            , 'message'     : phone_validator.message
            }
        )
    )

    telefono_3 = forms.CharField(
        required   = False,
        max_length=MAXTELEFONO,
        validators = [phone_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Teléfono 3'
            , 'pattern'     : phone_validator.regex.pattern
            , 'message'     : phone_validator.message
            }
        )
    )

    email_1 = forms.EmailField(
        required = False,
        max_length=MAXMAIL,
        widget   = forms.EmailInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'E-mail 1'
            , 'message'     : 'La entrada debe ser un e-mail válido.'
            }
        )
    )

    email_2 = forms.EmailField(
        required = False,
        max_length=MAXMAIL,
        widget   = forms.EmailInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'E-mail 2'
            , 'message'     : 'La entrada debe ser un e-mail válido.'
            }
        )
    )
    
class PropietarioForm(forms.Form):

    name_validator = RegexValidator(
        regex   = '^[\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
        message = 'La entrada debe ser un nombre en Español sin símbolos especiales.'
    )
    
    nombres = forms.CharField(
        required = True,
        max_length=MAXNOMBRE,
        label    = "Nombres del propietario",
        validators = [name_validator],
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Nombres del propietario'
            , 'pattern'     : name_validator.regex.pattern
            , 'message'     : name_validator.message
            }
        )
    )
    
    apellidos = forms.CharField(
        required = True,
        max_length=MAXNOMBRE,
        label    = "Apellidos del propietario",
        validators = [name_validator],
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Apellidos del propietario'
            , 'pattern'     : name_validator.regex.pattern
            , 'message'     : name_validator.message
            }
        )
    )
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )
    
    cedula = forms.CharField(
        required   = True,
        max_length=MAXCEDULA,
        label      = "Cédula",
        validators = [id_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cédula'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message
            }
        )
    )
    
    phone_validator = RegexValidator(
        regex   = '^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-?\d{7}',
        message = 'Debe introducir un formato válido de teléfono.'
    )
        
    telefono_1 = forms.CharField(
        required   = False,
        max_length=MAXTELEFONO,
        validators = [phone_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Teléfono 1'
            , 'pattern'     : phone_validator.regex.pattern
            , 'message'     : phone_validator.message
            }
        )
    )
class PuestosForm(forms.Form):
    
    particulares = forms.IntegerField(
        required  = True,
        min_value = 0,
        label     = 'Número de puestos particulares',
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Para particulares'
            , 'min'         : "0"
            , 'pattern'     : '^[0-9]+'
            , 'message'     : 'Debe ser un número entero no negativo.'
            }
        )
    )
        
    motos = forms.IntegerField(
        required  = True,
        min_value = 0,
        label     = 'Número de Puestos',
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Para motos'
            , 'min'         : "0"
            , 'pattern'     : '^[0-9]+'
            , 'message'     : 'Debe ser un número entero no negativo.'
            }
        )
    )
    
    camiones = forms.IntegerField(
        required  = True,
        min_value = 0,
        label     = 'Número de Puestos',
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Para camiones'
            , 'min'         : "0"
            , 'pattern'     : '^[0-9]+'
            , 'message'     : 'Debe ser un número entero no negativo.'
            }
        )
    )
    
    discapacitados = forms.IntegerField(
        required  = True,
    
        min_value = 0,
        label     = 'Número de Puestos',
        widget    = forms.NumberInput(attrs=
            { 'class'       : 'form-control'
            , 'placeholder' : 'Para discapacitados'
            , 'min'         : "0"
            , 'pattern'     : '^[0-9]+'
            , 'message'     : 'Debe ser un número entero no negativo.'
            }
        )
    )
class EstacionamientoExtendedForm(forms.Form):
    
    tarifa_validator = RegexValidator(
        regex   = '^([0-9]+(\.[0-9]+)?)$',
        message = 'Sólo debe contener dígitos.'
    )    
    
    puestos = forms.IntegerField(
        required = False,
        widget   = forms.HiddenInput()
    )
    puestos_C = forms.IntegerField(
        required = False,
        widget   = forms.HiddenInput()
    )
    puestos_M = forms.IntegerField(
        required = False,
        widget   = forms.HiddenInput()
    )
    puestos_D = forms.IntegerField(
        required = False,
        widget   = forms.HiddenInput()
    )
    
    horarioin = forms.TimeField(
        required = True,
        label    = 'Horario Apertura',
        widget   = forms.TimeInput(attrs =
            { 'class':'form-control'
            , 'placeholder' : 'Horario Apertura'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }, 
            format='%H:%M'
        )
    )

    horarioout = forms.TimeField(
        required = True,
        label    = 'Horario Cierre',
        widget   = forms.TimeInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Cierre'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }, 
            format='%H:%M'
        )
    )

    choices_esquema = [
        ('TarifaHora', 'Por hora'),
        ('TarifaMinuto', 'Por minuto'),
        ('TarifaHorayFraccion', 'Por hora y fracción'),
        ('TarifaHoraPico', 'Diferenciada por horario pico'),
        ('TarifaFinDeSemana', 'Diferenciada para fines de semana')
    ]

    feriados = forms.CharField(
        required = False,
        initial  = '2015-05-01,2015-06-24,2015-07-05,2015-07-24,2015-10-12,2015-12-25',
        widget   = forms.HiddenInput()
    )

    esquema = forms.ChoiceField(
        required = True,
        choices  = choices_esquema,
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )
    
    tarifa = forms.DecimalField(
        required   = True,
        validators = [tarifa_validator],
        widget     = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Tarifa'
            , 'pattern'     : '^([0-9]+(\.[0-9]+)?)$'
            , 'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    tarifa2 = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa 2',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )

    inicioTarifa2 = forms.TimeField(
        required = False,
        label    = 'Inicio Horario Especial',
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Inicio Reserva'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )

    finTarifa2 = forms.TimeField(
        required = False,
        label    = 'Fin Horario Especial',
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Fin Reserva'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )
    
    esquemaFeriados = forms.ChoiceField(
        required = False,
        choices  = choices_esquema,
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )
    
    tarifaFeriados = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa feriados',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )
    
    tarifaFeriados2 = forms.DecimalField(
            required   = False,
            validators = [tarifa_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Tarifa 2',
                'pattern'     : '^([0-9]+(\.[0-9]+)?)$',
                'message'     : 'La entrada debe ser un número decimal.'
            }
        )
    )
    
    inicioTarifaFeriados = forms.TimeField(
        required = False,
        label    = 'Inicio Horario Especial',
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Inicio Reserva'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )

    finTarifaFeriados = forms.TimeField(
        required = False,
        label    = 'Fin Horario Especial',
        widget   = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Horario Fin Reserva'
            , 'pattern'     : '^([0-1]?[0-9]|2[0-3]):[0-5][0-9]'
            , 'message'     : 'La entrada debe ser una hora válida.'
            }
        )
    )

class ReservaForm(forms.Form):
    
    vehiculoTipo = forms.ChoiceField(
        required = True,
        label    = 'Tipo de vehiculo',
        choices  = (
            ('Particular',  ''),
            ('Moto', ''),
            ('Camion', ''),
            ('Dicapacitado', '')
        ),
        widget  = forms.RadioSelect()
    )

    inicio = forms.SplitDateTimeField(
        required = True,
        label = 'Horario Inicio Reserva',
        widget= CustomSplitDateTimeWidget(attrs=
            { 'class'       : 'form-control'
            , 'type'        : 'date'
            , 'placeholder' : 'Hora Inicio Reserva'
            }
        )
    )

    final = forms.SplitDateTimeField(
        required = True,
        label    = 'Horario Final Reserva',
        widget   = CustomSplitDateTimeWidget(attrs=
            { 'class'       : 'form-control'
            , 'type'        : 'date'
            , 'placeholder' : 'Hora Final Reserva'
            }
        )
    )

class PagoForm(forms.Form):
    
    card_name_validator = RegexValidator(
        regex   = '^[\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
        message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    card_surname_validator = RegexValidator(
        regex   = '^[\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
        message = 'El apellido no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'Solo puede contener caracteres numéricos.'
    )
    
    card_validator = RegexValidator(
        regex   = '^[0-9]{16}$',
        message = 'Introduzca un número de tarjeta válido de 16 dígitos.'
    )
    
    pin_validator = RegexValidator(
        regex   = '^[0-9]{4}$',
        message = 'Introduzca un número de pin válido de 4 dígitos.'
    )
    
    nombre = forms.CharField(
        required   = True,
        max_length=MAXNOMBRE,
        label      = "Nombre del Tarjetahabiente",
        validators = [card_name_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Nombre del Tarjetahabiente'
            , 'pattern'     : card_name_validator.regex.pattern
            , 'message'     : card_name_validator.message
            }
        )
    )

    apellido = forms.CharField(
        required   = True,
        max_length=MAXNOMBRE,
        label      = "Apellido del Tarjetahabiente",
        validators = [card_surname_validator],
        widget = forms.TextInput(attrs =
            { 'class'      : 'form-control'
            , 'placeholder' : 'Apellido del Tarjetahabiente'
            , 'pattern'     : card_surname_validator.regex.pattern
            , 'message'     : card_surname_validator.message
            }
        )
    )

    cedulaTipo = forms.ChoiceField(
        required = True,
        label    = 'cedulaTipo',
        choices  = (
            ('V', 'V'),
            ('E', 'E')
        ),
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )

    cedula = forms.CharField(
        required   = True,
        max_length=MAXCEDULA,
        label      = "Cédula",
        validators = [id_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cédula'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message
            }
        )
    )

    tarjeta = forms.CharField(
        required   = False,
        max_length=MAXTARJETA,
        label      = "Tarjeta de Credito", 
        validators = [card_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Numero de Tarjeta'
            , 'pattern'     : card_validator.regex.pattern
            , 'message'     : card_validator.message
            }
        )
    )
    
    PIN = forms.CharField(
        required   = False,
        max_length = MAXPIN,
        label      = "Pin Billetera", 
        validators = [pin_validator],
        widget = forms.PasswordInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Pin de la billetera'
            , 'pattern'     : pin_validator.regex.pattern
            , 'message'     : pin_validator.message
            }
        )
    )
    
    ID = forms.CharField(
        required   = False,
        max_length = MAXID,
        label      = "ID Billetera", 
        validators = [id_validator],
        widget = forms.PasswordInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'ID de la billetera'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message
            }
        )
    )
    
    tarjetaTipo = forms.ChoiceField(
        required = True,
        label    = 'tarjetaTipo',
        choices  = (
            ('Vista',  ' VISTA '),
            ('Mister', ' MISTER '),
            ('Xpress', ' XPRESS '),
            ('Billetera Electronica', ' E-Wallet ')
        ),
        widget   = forms.RadioSelect()
    )

class RifForm(forms.Form):
    
    rif_validator = RegexValidator(
        regex   = '^[JVD]-\d{8}-?\d$',
        message = 'Introduzca un RIF con un formato válido de la forma X-xxxxxxxxx.'                              
    )
    
    rif = forms.CharField(
        required   = True,
        max_length=MAXRIF,
        label      = "RIF",
        validators = [rif_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'RIF: X-xxxxxxxxx'
            , 'pattern'     : rif_validator.regex.pattern
            , 'message'     : rif_validator.message
            }
        )
    )

class CedulaForm(forms.Form):
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )
    
    cedula = forms.CharField(
        required   = True,
        max_length=MAXCEDULA,
        label      = "Cédula",
        validators = [id_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cédula'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message
            }
        )
    )

# validacion del pin de la billetera
# va aqui o dentro de pago?
    
class BilleteraForm(forms.Form):
    
    name_validator = RegexValidator(
        regex   = '^[\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
        message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    surname_validator = RegexValidator(
        regex   = '^[\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
        message = 'El apellido no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    ci_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'La cédula solo puede contener caracteres numéricos.'
    )
    
    PIN_validator = RegexValidator(
        regex   = '^[0-9]{4}$',
        message = 'Su PIN solo puede contener 4 caracteres numéricos.'
    )
    
    nombre = forms.CharField(
        required   = True,
        max_length=MAXNOMBRE,
        label      = "Nombre del Tarjetahabiente",
        validators = [name_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Nombre del Tarjetahabiente'
            , 'pattern'     : name_validator.regex.pattern
            , 'message'     : name_validator.message
            }
        )
    )

    apellido = forms.CharField(
        required   = True,
        max_length=MAXNOMBRE,
        label      = "Apellido del Tarjetahabiente",
        validators = [surname_validator],
        widget = forms.TextInput(attrs =
            { 'class'      : 'form-control'
            , 'placeholder' : 'Apellido del Tarjetahabiente'
            , 'pattern'     : surname_validator.regex.pattern
            , 'message'     : surname_validator.message
            }
        )
    )
    
    cedula = forms.CharField(
        required   = True,
        max_length=MAXCEDULA,
        label      = "Cédula",
        validators = [ci_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cédula'
            , 'pattern'     : ci_validator.regex.pattern
            , 'message'     : ci_validator.message
            }
        )
    )
    
    PIN = forms.CharField(
        required   = True,
        max_length = MAXPIN,
        label      = "PIN",
        validators = [PIN_validator],
        widget = forms.PasswordInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'PIN'
            , 'pattern'     : PIN_validator.regex.pattern
            , 'message'     : PIN_validator.message
            }
        )
    )
    
    cedulaTipo = forms.ChoiceField(
        required = True,
        label    = 'cedulaTipo',
        choices  = (
            ('V', 'V'),
            ('E', 'E')
        ),
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )
    

class authBilleteraForm(forms.Form):
    PIN_validator = RegexValidator(
        regex   = '^[0-9]{4}$',
        message = 'Su PIN solo puede contener 4 caracteres numéricos.'
    )
    
    ID_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'Su ID solo puede contener 4 caracteres numéricos.'
    )
    
    ID = forms.CharField(
        required   = True,
        max_length = MAXID,
        label      = "ID",
        validators = [ID_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Introduzca el ID'
            , 'pattern'     : ID_validator.regex.pattern
            , 'message'     : ID_validator.message
            }
        )
    )
    
    Pin = forms.CharField(
        required   = True,
        max_length = MAXPIN,
        label      = "Pin",
        validators = [PIN_validator],
        widget = forms.PasswordInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'PIN'
            , 'pattern'     : PIN_validator.regex.pattern
            , 'message'     : PIN_validator.message
            }
        )
    )
    
class BilleteraPagoForm(forms.Form):
    card_name_validator = RegexValidator(
        regex   = '^[\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
        message = 'El nombre no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    card_surname_validator = RegexValidator(
        regex   = '^[\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ][\'\-A-Za-záéíóúñÑÁÉÍÓÚäëïöüÄËÏÖÜ ]*$',
        message = 'El apellido no puede iniciar con espacio en blanco ni contener números ni caracteres desconocidos.'
    )
    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'Solo puede contener caracteres numéricos.'
    )
    
    card_validator = RegexValidator(
        regex   = '^[0-9]{16}$',
        message = 'Introduzca un número de tarjeta válido de 16 dígitos.'
    )
    
    monto_validator = RegexValidator(
        regex   = '^([0-9]+(\.[0-9]+)?)$',
        message = 'La entrada debe ser un numero decimal separado por un punto.'
    )
    
    nombre = forms.CharField(
        required   = True,
        max_length=MAXNOMBRE,
        label      = "Nombre del Tarjetahabiente",
        validators = [card_name_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Nombre del Tarjetahabiente'
            , 'pattern'     : card_name_validator.regex.pattern
            , 'message'     : card_name_validator.message
            }
        )
    )

    apellido = forms.CharField(
        required   = True,
        max_length=MAXNOMBRE,
        label      = "Apellido del Tarjetahabiente",
        validators = [card_surname_validator],
        widget = forms.TextInput(attrs =
            { 'class'      : 'form-control'
            , 'placeholder' : 'Apellido del Tarjetahabiente'
            , 'pattern'     : card_surname_validator.regex.pattern
            , 'message'     : card_surname_validator.message
            }
        )
    )

    cedulaTipo = forms.ChoiceField(
        required = True,
        label    = 'cedulaTipo',
        choices  = (
            ('V', 'V'),
            ('E', 'E')
        ),
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )

    cedula = forms.CharField(
        required   = True,
        max_length=MAXCEDULA,
        label      = "Cédula",
        validators = [id_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cédula'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message
            }
        )
    )
    
    monto = forms.DecimalField(
            required   = True,
            max_digits = MAXMONTO,
            decimal_places = MAXDECIMALS,
            max_value = SMAX,
            label = "Monto de Recarga",
            validators = [monto_validator],
            widget     = forms.TextInput(attrs = {
                'class'       : 'form-control',
                'placeholder' : 'Monto a Recargar',
                'pattern'     : monto_validator.regex.pattern,
                'message'     : monto_validator.message
            }
        )
    )
    
    tarjeta = forms.CharField(
        required = True,
        max_length = MAXTARJETA,
        label      = "Tarjeta de Credito", 
        validators = [card_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Numero de Tarjeta'
            , 'pattern'     : card_validator.regex.pattern
            , 'message'     : card_validator.message
            }
        )
    )
    
    tarjetaTipo = forms.ChoiceField(
        required = True,
        label    = 'tarjetaTipo',
        choices  = (
            ('Vista',  ' VISTA '),
            ('Mister', ' MISTER '),
            ('Xpress', ' XPRESS ')
        ),
        widget   = forms.RadioSelect()
    )
    
    
class CancelaReservaForm(forms.Form):    
    id_validator = RegexValidator(
        regex   = '^[0-9]+$',
        message = 'Solo puede contener caracteres numéricos.'
    )
    
    ID = forms.CharField(
        required   = True,
        max_length = MAXID,
        label      = "ID",
        validators = [id_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Introduzca el ID'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message
            }
        )
    )
    
    cedulaTipo = forms.ChoiceField(
        required = True,
        label    = 'cedulaTipo',
        choices  = (
            ('V', 'V'),
            ('E', 'E')
        ),
        widget   = forms.Select(attrs =
            { 'class' : 'form-control' }
        )
    )

    cedula = forms.CharField(
        required   = True,
        max_length=MAXCEDULA,
        label      = "Cédula",
        validators = [id_validator],
        widget = forms.TextInput(attrs =
            { 'class'       : 'form-control'
            , 'placeholder' : 'Cédula'
            , 'pattern'     : id_validator.regex.pattern
            , 'message'     : id_validator.message
            }
        )
    )
