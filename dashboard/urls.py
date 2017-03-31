from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'),
	url(r'^formReport/$', views.formcharts, name='formcharts'),
	url(r'^report/$', views.charts, name='charts'),
]