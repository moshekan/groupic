from django.shortcuts import render
from annoying.decorators import ajax_request, render_to
from get_instagram_data import FILENAME
import json
import os.path as path
FILENAME=path.join(path.dirname(path.realpath(__file__)), FILENAME)


@render_to('landing.html')
def landing(request):
	return {}

@render_to('events.html')
def index(request):
	context = {"events" : get_json_data(FILENAME)}
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


