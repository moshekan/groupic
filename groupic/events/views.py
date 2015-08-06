from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from annoying.functions import get_object_or_None

from annoying.decorators import ajax_request, render_to
from get_instagram_data import FILENAME
from django.core import serializers
from events.models import Media
from models import Event

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
	events = Event.objects.all() or {}
	return {"events": serializers.serialize("json", events)}

def event_detail_live(request):
	event_id = request.Get.get('event_id')
	event = Event.objects.get(str_id=str_id)
	return event.media_set.all()
		

def get_json_data(filename):
	with open(filename) as f:
		return json.loads(f.read())
			

#SUNDAY DEMO

#@ajax_request
#def upload_image(request):
#	if request.method == 'POST':
#		image = Media(request.POST, request.FILES)
#		image.save()

@require_http_methods(["POST"])
@ajax_request
def upload_image(request):
	success = True
	error_msg = ""	
	try:
		event_id = request.POST.get('event_id')
		# TODO ensure user is part of the event
		media = Media(groupic=request.user.groupic, event=Event.objects.get(str_id=event_id))
    		media.save()
    		filename = 'groupic/event/static/events/images/{0}.png'.format(media.id)
    		media.full_res = filename
		# TODO create a real thumbnail			
		media.thumbnail = filename
    		media.save()
		handle_uploaded_file(request.FILES['media_data'], filename)
	except ObjectDoesNotExist:
		success = False
		error_msg = "Event %s does not exist" % event_id
		
	except Exception as e:
		success = False
		error_msg = str(e)
	return { 'success' : success, 'error_msg': error_msg}

def handle_uploaded_file(f, filename):
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
@require_http_methods(["POST"])
@ajax_request
def join_private_event(request):
    success = True
    error_msg = ""
    event = {}		
    try:
        barcode = request.POST.get('barcode')
        event = Event.objects.get(barcode=barcode)
        event.users.add(request.user)
        event.save()
    except ObjectDoesNotExist:
		success = False
		error_msg = "Barcode wasn't found"
    except Exception as e:
		success = False
		error_msg = str(e)
    return { 'success' : success, 'error_msg': error_msg, 'event' : serializers.serialize("json", event)}

@ajax_request
def view_images(request):
	str_id = request.GET.get('event_id')
	event = get_object_or_None(Event, str_id=str_id)
	if event:    	
		media = event.media_set.all()
	else:
		media = []  
	return {'media' : serializers.serialize("json", media)}

