 django.shortcuts import render

from annoying.decorators import ajax_request, render_to
from get_instagram_data import FILENAME
from django.core import serializers
#from models.py import Media
#from models.py import Event

import json
import os.path as path
FILENAME=path.join(path.dirname(path.realpath(__file__)), FILENAME)


@render_to('index.html')
def newIndex(request):
	context = {"events" : get_json_data(FILENAME),
	'nav_home':'active'}
	return context

@render_to('features.html')
def features(request):
	return {'nav_features':'active'}

@render_to('contact_us.html')
def contact_us(request):
	return {'nav_contact':'active'}

@render_to('about_us.html')
def about_us(request):
	return {'nav_about':'active'}

@render_to('events.html')
def index(request):
	context = {"events" : get_json_data(FILENAME),
	'nav_home':'active'}
	return context


@ajax_request
def events(request):
	return get_json_data(FILENAME)

@ajax_request
def event_detail(request):
	event_name=request.GET.get('event_name')
	data = get_json_data(FILENAME)
	if event_name is None:
		return data.values()[0]
	return data[event_name]
	

def get_json_data(filename):
	with open(filename) as f:
		return json.loads(f.read())

def json_to_db(filename):
	data = get_json_data(FILENAME)
	for key, value in data:
		for media in value:
			

#SUNDAY DEMO

#@ajax_request
#def upload_image(request):
#	if request.method == 'POST':
#		image = Media(request.POST, request.FILES)
#		image.save()


@ajax_request
def upload_image(request):
	if request.method == 'POST':
        	try:
        	    media = Media(groupic=user.groupic,url = 			    url, created_at=datetime.datetime.now(pytz.UTC))
            		drawing.save()
            		filename = 'groupic/event/static/events/images/{0}.png'.format(drawing.id)
            		drawing.filename=filename
            		drawing.save()
        	except:
            		response { 'success' : False, 'message' : "the drawings didnt save"}
        		handle_uploaded_file(request.FILES['file'], filename)
        	return { 'success' : True}
	
    		else:
    	   		return { 'success' : False, 'message' : "the immage didnt post"}


def handle_uploaded_file(f, filename):
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@ajax_request
def join_private_event(request):
	bcode = request.PUT.get('barcode')
	event = Event.objects.get(barcode=bcode)
	event.users.add(request.user)
	event.save()
	return serializers.serialize("json", event)

@ajax_request
def view_images(request):
	eventID = request.PUT.get('event_id')
	event = Event.objects.get(pk=eventID)
	return serializers.serialize("json", event.photo.all())


