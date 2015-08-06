from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'events$', views.events, name='events'),
	url(r'^contact_us$', views.contact_us, name='contact_us'),
	url(r'^features$', views.features, name='features'),
	url(r'^about$', views.about_us, name='about_us'),
	url(r'^new$', views.newIndex, name='new'),
	url(r'^upload$', views.upload_image, name='upload_image'),
	url(r'join_private$', views.join_private_event, name='join_private_event'),
	url(r'view_images$', views.view_images, name='view_images'),
    	url(r'^$', views.index, name='index'),


]
