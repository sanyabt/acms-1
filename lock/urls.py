from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^results/$', views.results, name='results'),
    url(r'^item/$', views.item, name='item'),
    url(r'^success/(?P<quantity>[0-9]+)/(?P<name>[0-9]+)/$', views.success, name='success'),
    url(r'^fail/$', views.success, name='fail'),	
]