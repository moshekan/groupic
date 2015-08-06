from collections import Counter
from events.models import Media
from events.models import Event
import datetime
import glob
import json
from instagram.client import InstagramAPI
from geopy.geocoders import Nominatim




DISTANCE = 1500

TEL_AVIV = (32.085300, 34.781768)
RIO = (-22.906847, -43.172896)
LONDON = (51.507351, -0.127758)
GAZA = (31.354676, 34.308826)
JERUSALEM = (31.768319, 35.213710)
RAMALLAH = (31.898043, 35.204271) 
GREEK = (40.700880, -79.321925)
ISRAEL = (31.046051, 34.851612)
SOUTH_AMERICA = (-8.783195, -55.491477)
GLENDALE = (33.538652, -112.185987)
ARIZONA = (34.048928, -111.093731)
ORACLE_ARENA = (37.750268, -122.202609)
QUICKEN_LOANS_ARENA = (41.496577, -81.688076)
VIENNA = (48.208174, 16.373819)
SYRIA = (34.802075, 38.996815)


EVENTS = {
# 'gaza-war-2015': {'tags': {'gaza','gaza4life','gazawillbefree','gazaunderattack'},
# 		'locations': [GAZA, JERUSALEM, RAMALLAH],
# 		'name': "Gaza War 2015"
# 		},
'olympics-summer-2012': {'tags': {'olympics', 'olympics2012', 'olympicsherewecome'}, 
		'locations': [LONDON],
		'name': "The Olympic Games 2012"
		},
# 'fifa-world-cup-2014': {'tags': {'fifaworldcup', 'worldcup', 'fifaworldcup2014', 'fifaworldclupbrasil2014'},
# 			'locations': [RIO],
# 			'name': "Fifa World Cup"
# 			},
'gay-pride-israel-2015': {'tags': {'gay', 'gaypride', 'gayprideisrael', 'israel', 'israelgayparade', 'gayprideparade', 'gaypride2015', 'gayparade2015', 'gayprideisrael'}, 		
			'locations': [TEL_AVIV],
		'name': "Gay Pride 2015",
		},
'greek-crisis': {'tags': {'greek', 'greekcrisis', 'greekcrisiseffects', 'greekcrisis2015', 'greeklife'}, 
		'locations': [GREEK],
		'name': "Greek Crisis 2015"
		},
'israel-elections': {'tags': {'israel', 'israelelections', 'israelelections2015'},
		'locations': [ISRAEL],
		'name': "Israel Elections 2015"
		},
'2015-copa-america': {'tags': {'copaamerica', 'copaamerica2015', 'copaamericachile2015', 'copaamerica2015'},
		'locations': [SOUTH_AMERICA],
		'name': "Copa America 2015"
		},
'super-bowl': {'tags': {'superbowl', 'superbowlxlix', 'superbowlchamps', 'superbowl49', 'super_bowl2015', 
		'superbowl2015'},
		'locations': [ARIZONA],
		'name': "Super Bowl XLIX"
		},
'nba-finals': {'tags': {'nba', 'nbafinals', 'nba_finals'},
		'locations': [ORACLE_ARENA, QUICKEN_LOANS_ARENA],
		'name': "2015 NBA Finals"
		},
'eurovision': {'tags': {'eurovision', 'eurovision2015', 'eurovisionsongcontest', 'eurovisionsongcontest2015'},
		'locations': [VIENNA], 
		'name': "Eurovision Song Contest 2015"
		},
'syria-war-2015': {'tags': {'syria', 'syrianarabarmy', 'syrianrevolution', 'syriawaycrimes', 'syriafree', 
                            'syria_free', 'syriacrisis'},
		   'locations': [SYRIA],
		   'name': "Syria Civil War 2015"
		}

}
PATTERN  ='-chunk.json'
FILENAME="events.json-bak"
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


        


def write_to_file(filename, events):
    with open(filename, 'w') as f:
        f.write(json.dumps(byteify(events), indent=4, sort_keys=True))

def read_from_file(filename):
	with open(filename) as f:
    		return json.loads(f.read())

def combine_json_files(pattern=PATTERN, newfile=FILENAME):
    data={}
    for filename in glob.glob("*" + pattern):
        event_name = filename.split(pattern)[0]
        data[event_name] = read_from_file(filename)
    write_to_file(newfile, data)

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
def get_all_events(api):
    events = {}
    for event_name, event in EVENTS.iteritems():
        get_event(api, event_name, event)
    write_to_file(FILENAME, events)

def get_event(api, event_key, event):
    event_dict = get_event_dict(api, event)
    filename = event_key + PATTERN
    write_to_file(filename, {filename:event_dict})

def json_to_db(filename):
	data = read_from_file(filename)
	
	for key,value in data.iteritems():
		event = Event(str_id=key, name=value['name'], is_public=True)
		event.save()
		print "created event %s" %key
		for media in value['media']:
			media = Media(full_res=media['full_res'], thumbnail = media['thumbnail'], event=event)
			media.save()
if __name__ == "__main__":
    import sys
    api = InstagramAPI(access_token=ACCESS_TOKEN, client_secret=CLIENT_SECRET)
    if len(sys.argv) == 1 or sys.argv[1] == "--all":
        print "getting all events"
        get_all_events(api)
    else:
        event_key = sys.argv[1]
        event = EVENTS[event_key]
        print "getting event:", event['name']
        get_event(api, event_key, event)
