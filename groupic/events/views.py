from django.shortcuts import render
from annoying.decorators import ajax_request, render_to
from get_instagram_data import FILENAME
import json
import os.path as path
FILENAME=path.join(path.dirname(path.realpath(__file__)), FILENAME)

<<<<<<< HEAD

# Create your views here.
=======
@render_to('events.html')
>>>>>>> 70df198608645e4fa9d1702a610ef36df910ff23
def index(request):
	context = {"events" : [{"id":1, "eventName":"Maor"},{"id":2,"eventName":"Nadav"},{"id":3,"eventName":"Tamar"}]}
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


