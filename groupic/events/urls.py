from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^landing$', views.landing, name='landing'),
    	url(r'^$', views.index, name='index'),
	url(r'events', views.events, name='events'),
	url(r'event_detail', views.event_detail, name='event_detail'),
]
