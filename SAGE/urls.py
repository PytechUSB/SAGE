from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SAGEPhoenix.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', RedirectView.as_view(url='estacionamientos/', permanent=True)),
    url(r'^estacionamientos/', include('estacionamientos.urls')),
    url(r'^admin/', include(admin.site.urls))
)
