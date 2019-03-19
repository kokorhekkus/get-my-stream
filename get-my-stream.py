#!/usr/bin/python

# Download all the photos on my Flickr stream
import flickrapi
import urllib
import sys
import pprint

api_key = '9e340ba2325f072d3994e7be5fb8f02b'
api_secret = 'f3ede0e7cd1c808f'
if len(sys.argv) == 2:
    user_id = sys.argv[1]
else:
    print("Requires a single argument, which is your Flickr ID: quitting")
    quit()

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read') # needed to get my own non-public photos

# Get the urls for all the photos
per_page = 500
urls = {}
page = 1
while 1:
    # Note: url_o gets the URL for the original size image.  there are other options e.g. url_c for a compact image
    print("Getting page %d" % page)
    try:
        p = flickr.photos.search(user_id=user_id,per_page=per_page,page=page,extras='url_o',format='parsed-json')
    except Exception as e:
        print("Failed to retrieve photos from Flickr:")
        print(e)
        quit()

    photos = p['photos']['photo']
    for i in photos:
        try:
            url = i["url_o"]
            id = i["id"]
        except KeyError:
            print("Failed to get URL or id for this photo:")
            pprint.pprint(i)
        except Exception as e:
            print(e)

        urls[id] = url

    total_pages = p['photos']['pages']
    print("Total pages are %d" % total_pages)
    
    if(page == total_pages):
        break
    else:
        page += 1

# Open or create our file which keeps a record of what photos we've already downloaded
already_dled = []
for pic_id in open('id_data.txt','a+'):
    already_dled.append(pic_id)

# Download all the photos
f = open('id_data.txt','a')

for id, url in urls.items():
    if(id in already_dled):
        continue
    
    jpg_name = id + '.jpg'
    try:
        urllib.urlretrieve(url, jpg_name)
    except Exception as e:
        print("Could not retrieve photo at %s" % i)
        print(e)
        continue

    id_line = id + '\n'
    f.write(id_line)

f.close()
