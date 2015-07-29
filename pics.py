from instagram.client import InstagramAPI

access_token = "2047500927.3561200.794e724d28454fb19b92f10fbd11b90f"
client_secret = "07eba75913484e75bf71a12e8a5932ce"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
def get_pics_by_tag(tag):
	recent_media = api.tag_recent_media(30,0,tag)
	for media in recent_media[0]:
		print media.get_standard_resolution_url()
get_pics_by_tag("swag")
