# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from estacionamientos import views


# Este error es raro, en django funciona
urlpatterns = patterns('',
    url(r'^$', views.estacionamientos_all, name = 'estacionamientos_all'),
    url(r'^(?P<_id>\d+)/propietario-crear$', views.propietario_all, name = 'propietario_all'),
    url(r'^propietario-crear$', views.propietario_all, name = 'propietario_all'),
    url(r'^propietario/(?P<_id>\d+)/$', views.propietario_edit, name = 'propietario_edit'),
    url(r'^(?P<_id>\d+)/$', views.estacionamiento_detail, name = 'estacionamiento_detail'),
    url(r'^(?P<_id>\d+)/cambiar-dueno', views.estacionamiento_edit, name = 'estacionamiento_edit'),
    url(r'^(?P<_id>\d+)/reserva$', views.estacionamiento_reserva, name = 'estacionamiento_reserva'),
    url(r'^(?P<_id>\d+)/pago$', views.estacionamiento_pago, name = 'estacionamiento_pago'),
    url(r'^ingreso$', views.estacionamiento_ingreso, name = 'estacionamiento_ingreso'),
    url(r'^consulta_reserva$', views.estacionamiento_consulta_reserva, name = 'estacionamiento_consulta_reserva'),
    url(r'^sms$', views.receive_sms, name='receive_sms'),
    url(r'^(?P<_id>\d+)/tasa$', views.tasa_de_reservacion, name = 'tasa_de_reservacion'),
    url(r'^grafica/.*$', views.grafica_tasa_de_reservacion, name = 'grafica_tasa_de_reservacion'),
    url(r'^crear_billetera$', views.billetera_all, name = 'billetera_all'),
    url(r'^datos_billetera$', views.billetera_datos, name = 'billetera_datos'),
    url(r'^(?P<_id>\d+)/recarga_billetera$', views.billetera_recarga, name = 'billetera_recarga'),
    url(r'^validar_reserva$', views.validar_reserva, name = 'validar_reserva')
)
