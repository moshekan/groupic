from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^landing$', views.landing, name='landing'),
    	url(r'^$', views.index, name='index'),
	url(r'events', views.events, name='events'),
	url(r'event_detail', views.event_detail, name='event_detail'),
	url(r'^contact_us$', views.contact_us, name='contact_us'),
	url(r'^features$', views.features, name='features'),
	url(r'^about$', views.about_us, name='about_us'),


]
