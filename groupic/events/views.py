from django.shortcuts import render

# Create your views here.
def index(request):
	context = {"events" : [{"eventName":"Maor"},{"eventName":"Nadav"},{"eventName":"Tamar"}]}
	return render(request, 'events.html', context)