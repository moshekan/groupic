from django.db import models
#from django.contrib.gis.geos import Point
#from location_field.models.spatial import LocationField
from django.contrib.auth.models import User


class Event(models.Model):
	name = models.CharField(max_length=255)
	str_id = models.CharField(max_length=255)
	is_public = models.BooleanField(default=False)
	city = models.CharField(max_length = 255)
	#location = LocationField(based_fields=[city], zoom=7, default='Point(1.0 1.0)')
	#objects = models.GeoManager()
	users = models.ManyToManyField(User, related_name='user', blank=True, default = None)
	admin = models.ForeignKey(User, related_name='admin', null=True, blank=True, default = None)
	barcode = models.CharField(max_length=255)
	
	def __unicode__(self):
		return u"Event %s" % self.str_id

class Media(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	full_res = models.CharField(max_length=255)
	thumbnail =models.CharField(max_length=255)
	user = models.ForeignKey(User, null=True, blank=True, default=None)
	event = models.ForeignKey(Event)

	def __unicode__(self):
		return u"Media %s" % self.str_full_res
	

