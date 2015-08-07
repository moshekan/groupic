from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from annoying.functions import get_object_or_None

from annoying.decorators import ajax_request, render_to
from get_instagram_data import FILENAME
from django.core import serializers
from events.models import Media
from models import Event

import dropbox
import json
import os.path as path
FILENAME=path.join(path.dirname(path.realpath(__file__)), FILENAME)

import datetime


@render_to('index.html')
def newIndex(request):
	context = {"events" : get_serial_events(),
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

@render_to('index.html')
def index(request):
	context = {"events" : get_serial_events(),
	'nav_home':'active'}
	return context


@ajax_request
def events(request):
	return get_serial_events()


def get_json_data(filename):
	with open(filename) as f:
		return json.loads(f.read())

def get_serial_events():
	events = Event.objects.all() or {}
	return {event.str_id: event.serialize() for event in events }

#SUNDAY DEMO

#@ajax_request
#def upload_image(request):
#	if request.method == 'POST':
#		image = Media(request.POST, request.FILES)
#		image.save()

@require_http_methods(["POST"])
@ajax_request
@csrf_exempt
def upload_image(request):
	success = True
	error_msg = ""	
        obj_created = None
	try:
		event_id = request.POST.get('event_id')
		# TODO ensure user is part of the event
		media = Media(event=Event.objects.get(str_id=event_id))
                media.save()
		filename = handle_uploaded_file(request.FILES['media_data'], media.id)
		media.full_res = filename
		# TODO create a real thumbnail			
		media.thumbnail = filename
		media.save()
                obj_created = media.serialize()
	except ObjectDoesNotExist:
		success = False
		error_msg = "Event %s does not exist" % event_id
		
	except Exception as e:
		success = False
		error_msg = str(e)
        return { 'success' : success, 'error_msg': error_msg, 'obj_created': obj_created}

def handle_uploaded_file(f, media_id):
    if settings.DROPBOX_ACCESS_TOKEN is None:
        filename = '/static/events/images/gallery/{0}.png'.format(media_id)
        dst_filename = 'events' + filename
        write_file_to_disk(f, dst_filename)
        return filename
    else:
        filename = '{0}.png'.format(media_id)
        client = dropbox.client.DropboxClient(settings.DROPBOX_ACCESS_TOKEN)
        write_file_to_dropbox(client, f, filename)
        return get_dropbox_filename(client, filename)

def write_file_to_dropbox(client, f, filename):
    client.put_file(filename, f)

def get_dropbox_filename(client, filename):
    url = client.share(filename, short_url=False).get('url')
    url = url.replace("www.dropbox.com", "dl.dropboxusercontent.com") # raw image
    return url

def write_file_to_disk(f, filename):
	with open(filename, 'wb+') as dst:
		for chunk in f.chunks():
			dst.write(chunk)

@require_http_methods(["POST"])
@ajax_request
@csrf_exempt
def join_private_event(request):
	success = True
	error_msg = ""
	event = {}		
	try:
		barcode = request.POST.get('barcode')
		event = Event.objects.get(barcode=barcode)
		#event.users.add(auth.get_user(request))
	except ObjectDoesNotExist:
		success = False
		error_msg = "Barcode wasn't found for " + barcode
	except Exception as e:
		success = False
		error_msg = str(e)
	return { 'success' : success, 'error_msg': error_msg, 'event' : event.serialize()}

@ajax_request
def view_images(request):
	str_id = request.GET.get('event_id', request.GET.get('id'))
	timestamp = request.GET.get('timestamp')
	event = get_object_or_None(Event, str_id=str_id)
	if event:    	
		if timestamp is None:
			media = event.media_set.all()
		else:
			dt = datetime.datetime.fromtimestamp(int(timestamp)/1000.0)
			media = event.media_set.filter(created_at__gt=dt)
	else:
		media = []  
	return {'media' : map(lambda x: x.serialize(), reversed(media))}
