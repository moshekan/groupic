from django.db import models
from django.core import serializers
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
	users = models.ManyToManyField(User, related_name='user', blank=True)
	admin = models.ForeignKey(User, related_name='admin', null=True, blank=True, default = None)
	barcode = models.CharField(max_length=255)
	
	def serialize(self):
		return {
			'name': self.name,
			'str_id': self.str_id,
			'is_public':self.is_public,
			'city':self.city,
			'admin': serialize_user(self.admin),
			'media': map(lambda x: x.serialize(), self.media_set.all())
			}
			
	def __unicode__(self):
		return u"Event %s" % self.str_id

class Media(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	full_res = models.TextField()
	thumbnail =models.TextField()
	user = models.ForeignKey(User, null=True, blank=True, default=None)
	event = models.ForeignKey(Event)

	def serialize(self):
		return {
			'created_at': self.created_at,
			'full_res': self.full_res,
			'thumbnail': self.thumbnail,
			'user': serialize_user(self.user),
			'event': self.event.str_id
		}

	def __unicode__(self):
		return u"Media %s" % self.str_full_res

def serialize_user(user):
	if user:
		username = user.username
	else:
		username = None
	return {
		'username': username
	}
