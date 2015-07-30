from instagram.client import InstagramAPI
import json
import datetime
from geopy.geocoders import Nominatim



EVENTS = {
'gaza-war-2015': ['nofilter','dogs','party','germany'],
}

FILENAME="events.json"
ACCESS_TOKEN = "2047500927.3561200.794e724d28454fb19b92f10fbd11b90f"
CLIENT_SECRET = "07eba75913484e75bf71a12e8a5932ce"
LIKE_COUNT = 1
LIMIT = 50


def get_timestamp(dt):
	return int(dt.strftime("%s"))



def get_address(location):
	geolocator = Nominatim()
	latitude, longitude = location
 	address = ""
	if latitude is not None:
		address = geolocator.reverse(latitude, longitude).address
	return address
def get_pics_for_event(api, tags):
	media_list=[]
        for tag in tags:
		recent_media, _next = api.tag_recent_media(LIMIT,0,tag)
		while len(recent_media)<LIMIT:
    			more_media, _next = api.tag_recent_media(tag_name=tag, with_next_url=_next)
			recent_media.extend(more_media)

		recent_media = recent_media[:LIMIT]
		print "Searching tag %s. Found: %d items" % (tag, len(recent_media))
		for media in recent_media:
			if media.like_count > LIKE_COUNT:
				temp_dic={}
				temp_dic['full_res']= media.get_standard_resolution_url()
				temp_dic['thumbnail']= media.get_thumbnail_url()
				temp_dic['like_count']= media.like_count
				temp_dic['username']=media.user.username
				temp_dic['created_time']=get_timestamp(media.created_time)
				try:
					point = media.location.point
					temp_dic['location'] = get_address((point.latitude, point.longitude))
				except:
					temp_dic['location'] = ""
				media_list.append(temp_dic)
	return media_list
def get_events():
	api = InstagramAPI(access_token=ACCESS_TOKEN, client_secret=CLIENT_SECRET)
	events = {}
	for event_name,tags in EVENTS.iteritems():
		print "Searching event:", event_name
		events[event_name]=get_pics_for_event(api, tags)
	return events

def write_to_file(filename, events):
	with open(filename, 'w') as f:
		f.write(json.dumps(events))

if __name__ == "__main__":
	events = get_events()
	print events
	write_to_file(FILENAME, events)
