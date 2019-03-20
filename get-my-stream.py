#!/usr/bin/python

# Download all the photos on my Flickr stream
import flickrapi
import urllib
import sys
import pprint
import logging
logging.basicConfig(filename='get-my-stream.log',level=logging.DEBUG)

api_key = '9e340ba2325f072d3994e7be5fb8f02b'
api_secret = 'f3ede0e7cd1c808f'
if len(sys.argv) == 2:
    user_id = sys.argv[1]
else:
    print('Requires a single argument, which is your Flickr ID: quitting')
    quit()

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read') # needed to get my own non-public photos
logging.info('User is authenticated')

# Get the urls for all the photos
per_page = 500
urls = {}
page = 1
while 1:
    # Note: url_o gets the URL for the original size image.  there are other options e.g. url_c for a compact image
    logging.debug('Getting page %d', page)
    try:
        p = flickr.photos.search(user_id=user_id,per_page=per_page,page=page,extras='url_o',format='parsed-json')
    except Exception as e:
        logging.error('Failed to retrieve photos from Flickr:')
        logging.error(e)
        quit()

    photos = p['photos']['photo']
    for i in photos:
        try:
            url = i["url_o"]
            id = i["id"]
        except KeyError:
            logging.error('Failed to get URL or id for this photo:')
            logging.error(i)
        except Exception as e:
            logging.error(e)

        urls[id] = url

    total_pages = p['photos']['pages']
    logging.debug('Total pages are %d', total_pages)
    
    if(page == total_pages):
        break
    else:
        page += 1

logging.info('Got %d URLs', len(urls))

# Open or create our file which keeps a record of what photos we've already downloaded
already_dled = []
for pic_id in open('id_data.txt','a+'):
    already_dled.append(int(pic_id))
logging.debug('Read in id_data.txt, found %d ids', len(already_dled))
    
f = open('id_data.txt','a')

# Download all the photos
num_downloaded = 0
for id, url in urls.items():
    logging.debug('Id is %d', int(id))
    
    if(int(id) in already_dled):
        logging.debug('%s already downloaded, skipping', id)
        continue
    
    jpg_name = id + '.jpg'
    try:
        urllib.urlretrieve(url, jpg_name)
    except Exception as e:
        logging.error('Could not retrieve photo %s', id)
        logging.error(e)
        continue

    logging.debug('Downloaded photo %s', id)
    num_downloaded += 1
    id_line = id + '\n'
    f.write(id_line)

f.close()
logging.info('Downloaded %d photos', num_downloaded)
logging.info('Exit')
