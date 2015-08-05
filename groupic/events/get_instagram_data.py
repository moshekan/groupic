from instagram.client import InstagramAPI
import json
import datetime
from geopy.geocoders import Nominatim
from collections import Counter

DISTANCE = 1500

TEL_AVIV = (32.085300, 34.781768)
RIO = (-22.906847, -43.172896)
LONDON = (51.507351, -0.127758)
GAZA = (31.354676, 34.308826)
JERUSALEM = (31.768319, 35.213710)
RAMALLAH = (31.898043, 35.204271) 


EVENTS = {
'gaza-war-2015': {'tags': {'gaza','gaza4life','gazawillbefree','gazaunderattack'},
		'locations': [GAZA, JERUSALEM, RAMALLAH],
		'name': "Gaza War 2015"
		},
'olympics-summer-2012': {'tags': {'olympics', 'olympics2012', 'olympicsherewecome'}, 
		'locations': [LONDON],
		'name': "The Olympic Games 2012"
		},
'fifa-world-cup-2014': {'tags': {'fifaworldcup', 'worldcup', 'fifaworldcup2014', 'fifaworldclupbrasil2014'},
			'locations': [RIO],
			'name': "Fifa World Cup"
			},
'gay-pride-israel-2015': {'tags': {'gay', 'gaypride', 'gayprideisrael', 'israel', 'israelgayparade', 'gayprideparade', 'gaypride2015', 'gayparade2015', 'gayprideisrael'}, 		
			'locations': [TEL_AVIV],
		'name': "Gay Pride 2015",
		}
		
}

FILENAME="events.json"
ACCESS_TOKEN = "2047500927.3561200.794e724d28454fb19b92f10fbd11b90f"
CLIENT_SECRET = "07eba75913484e75bf71a12e8a5932ce"
LIKE_COUNT = 5
MEDIA_LIMIT = 50
PAGE_LIMIT = 5

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def get_timestamp(dt):
    return int(dt.strftime("%s"))


def get_address(location):
    geolocator = Nominatim()    
    latitude, longitude = location
    address = ""
    if latitude is not None:
        address = geolocator.reverse(latitude, longitude).address
    return address

def get_insta_location(api, location):
    lat, lng = location
    return api.location_search(lat=lat, lng=lng, distance=DISTANCE)

def get_media_from_location(api, location):
    recent_media, _next = api.location_recent_media(location_id=location.id)
    count = 0
    while count < PAGE_LIMIT:
        more_media, _next = api.location_recent_media(location_id=location.id, with_next_url= _next)
        recent_media.extend(more_media)
        count += 1
    return recent_media

def filter_by_tags(media, tags):
    # TODO: get better tags
    return media
    filtered_media = []
    for photo in media:
        my_tags = set(photo.tags)
        if len(tags.intersection(my_tags)) > 0:
            filtered_media.append(photo)
    return filtered_media

def filter_by_like_count(media):
    # TODO: get more media
    return media
    return filter(lambda x: x > LIKE_COUNT, media)

def media_as_dict(media_list):
    media_dicts = []
    for media in media_list:
        media_dict={}
        media_dict['full_res']= media.get_standard_resolution_url()
        media_dict['thumbnail']= media.get_thumbnail_url()
        media_dict['like_count']= media.like_count
        media_dict['username']=media.user.username
        media_dict['created_time']=get_timestamp(media.created_time)
        media_dict['tags'] = [tag.name for tag in media.tags]
        try:
            point = media.location.point
            media_dict['location'] = get_address((point.latitude, point.longitude))
        except:
            media_dict['location'] = ""
            media_dicts.append(media_dict)
    return media_dicts

    

def get_event_dict(api, event):
    locations = event['locations']
    tags = event['tags']
    print "#1. get locations"
    insta_locations = []
    for location in locations:
        insta_locations.extend(get_insta_location(api, location))
    print '#2. search locations for media'
    media_list=[]
    print "Number of locations:", len(insta_locations)
    for location in insta_locations:
        print "Searching location..."
        media_list.extend(get_media_from_location(api, location))
        
    media_list=set(media_list)
    
    print "Total media count:", len(media_list)
    print '#3. filter tags'
    
    media_list = filter_by_tags(media_list, tags)
    print "Total media count:", len(media_list)
    
    print '#4. filter by likes'
    media_list = filter_by_like_count(media_list)
    
    print "Total media count:", len(media_list)
    print '#5. extract json'
    return {'media' : media_as_dict(media_list),
	    'name' : event['name']}


        
def get_events():
    api = InstagramAPI(access_token=ACCESS_TOKEN, client_secret=CLIENT_SECRET)
    events = {}
    for event_name, event in EVENTS.iteritems():
        print "Searching event:", event_name
        events[event_name]=get_event_dict(api, event)
    return events

def write_to_file(filename, events):
    with open(filename, 'w') as f:
        f.write(json.dumps(byteify(events)))

def read_from_file(filename):
	with open(filename) as f:
    		return json.loads(f.read())
def get_tags_counter(events):
	all_tags = {}

	for event_name, media in events.iteritems():
		tags = []
		for m in media:
			tags.extend(m['tags'])
		all_tags[event_name] = Counter(tags)
	return all_tags
		
def print_most_common_tags(counters, top_count=10):
	for event_name, counter in counters.iteritems():
		for tag, count in counter.most_common(top_count):
			print "%s\t%s" % (tag, count)

if __name__ == "__main__":
    events = get_events()
    print events
    write_to_file(FILENAME, events)
