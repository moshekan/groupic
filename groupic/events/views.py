from django.shortcuts import render

# Create your views here.
def index(request):
	context = {"events" : [{"id":1, "eventName":"Maor"},{"id":2,"eventName":"Nadav"},{"id":3,"eventName":"Tamar"}]}
	return render(request, 'events.html', context)