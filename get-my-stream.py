# Download all the photos on my Flickr stream

import flickrapi
import urllib
import json

api_key = '9e340ba2325f072d3994e7be5fb8f02b'
api_secret = 'f3ede0e7cd1c808f'
user_id = '44176346@N00' # my user

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read')

p = flickr.photos.search(user_id='44176346@N00',per_page=5,extras='url_c',format='parsed-json')
photos = p['photos']['photo']

urls = []
for i in photos:
    url = i["url_c"]
    urls.append(url)

urllib.urlretrieve(urls[1], '00001.jpg')
