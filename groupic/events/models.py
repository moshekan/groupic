#from django.db import models
#from django.contrib.gis.geos import Point
#from location_field.models.spatial import LocationField
#from django.contrib.auth.models import User


#class Event(models.Model):
#	event_name = models.CharField(max_length=255)
#	is_public = models.BooleanField(default=False)
#	city = models.CharField(max_legth = 255)
#	location = LocationField(based_fields=[city], zoom=7 default='Point(1.0 1.0)')
#	objects = models.GeoManager()
#	users = models.ManyToManyField(User)
#	admin = models.ForeignKey(User)
		

#class Media(models.Model):
#	created_at = models.DateTimeField(auto_now_add=True)
#	url = models.CharField(max_legth = 255)
#	user = models.ForeignKey(User)
#	event = models.ForeignKey(Event)

#---------------------------------------------------

#from django.db import models
#from django.contrib.auth.models import User


#class Twisser(models.Model):
#    user = models.OneToOneField(User)
 #   nationality = models.CharField(max_length=50)
  #  twissies = models.IntegerField(default=0)

#class Drawing(models.Model):
 #   twisser = models.ForeignKey(Twisser)
  #  filename = models.CharField(max_length=100)
   # score = models.IntegerField(default=0)
    #category = models.CharField(max_length=20)
    #is_public = models.BooleanField(default=False)
    #date = models.DateTimeField()

    #def serialize(self):
     #   d = {
      #      'twisser_id': self.twisser.id,
       #     'filename' : self.filename,
        #    'score' : self.score,
         #   'category' : self.category,
          #  'is_public' : self.is_public,
           # 'date' : str(self.date),
            #'drawing_id' : self.id,
      #  }
       # return d

	


