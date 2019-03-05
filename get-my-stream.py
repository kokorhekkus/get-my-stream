# Download all the photos on my Flickr stream
import flickrapi
import urllib
import sys

api_key = '9e340ba2325f072d3994e7be5fb8f02b'
api_secret = 'f3ede0e7cd1c808f'
if len(sys.argv) == 2:
    #user_id = '44176346@N00'
    user_id = sys.argv[1]
else:
    print("Requires a single argument, which is your Flickr ID: quitting")
    quit()

print(user_id)
flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read') # needed to get my own non-public photos

# Get the urls for all the photos
per_page = 500
urls = []
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
            urls.append(url)
        except KeyError:
            print("Failed to get URL for this photo:")
            print(i)
        except Exception as e:
            print(e)

    p2 = p['photos']
    total_pages = p2['pages']
    print("Total pages are %d" % total_pages)
    
    if(page == total_pages):
        break
    else:
        page += 1
        
# Download all the photos
photo_number = 1
for i in urls:
    jpg_name = str(photo_number) + '.jpg'
    try:
        urllib.urlretrieve(i, jpg_name)
    except Exception as e:
        print("Could not retrieve photo at %s" % i)
        print(e)
        quit()

    photo_number += 1


# Example dict:

#{u'photos': {u'page': 1,
#            u'pages': 2081,
#            u'perpage': 1,
#            u'photo': [{u'farm': 8,
#                     u'height_o': u'1944',
#                     u'id': u'47185604961',
#                     u'isfamily': 1,
#                     u'isfriend': 1,
#                     u'ispublic': 0,
#                     u'owner': u'44176346@N00',
#                     u'secret': u'899e269c9d',
#                     u'server': u'7881',
#                     u'title': u'Car selfie',
#                     u'url_o': u'https://farm8.staticflickr.com/7881/47185604961_e6d8b05338_o.jpg',
#                     u'width_o': u'2592'}],
#u'total': u'2081'},
#u'stat': u'ok'}
