from django.db import models

class Event(models.Model):
	event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50)
    event_type = models.IntegerField(max_length=1)
    users = models.ManyToMantField(Users)
    media = models.ManyToMantField(Media)
    admins = models.ManyToMantField(Admins)
    location = 10

# Create your models here.
