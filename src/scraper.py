from bs4 import BeautifulSoup
from urllib import urlretrieve
import urllib2 as urllib
import urlparse
import os
import sys

def create_url(url):
	if 'http:' not in url and 'https:' not in url:
		url = 'http://' + url
	return url

def valid_url(check_url):
	try:
		check_url = create_url(check_url)
		urllib.urlopen(urllib.Request(check_url))
		return True
	except:
		return False

def urls(soup):
	url_tags = soup.find_all('a')
	for tag in url_tags:
		try:
			link = tag['href']
			if 'www' in link:
				link = link[link.index('www'):]
			elif link[0] == '/':
				link = url + link
			if(valid_url(link)):
				with open("urls.txt", "a") as myfile:
					myfile.writelines(link + '\n')
		except:
			print 'error'
	print 'Links Done'

def images(soup):
	i = 1
	img_tags = soup.find_all('img')
	if not os.path.exists('images'):
		os.makedirs('images')

	for image in img_tags:
		try :
			if(valid_url(image['src'])):
				image_url = urlparse.urljoin(url, image['src'])
				urlretrieve(image_url, "images/image" + str(i) + ".jpg")
				i+=1
			else:
				print 'invalid url'
		except:
			print 'error'
	print 'Images Done'

url = create_url(sys.argv[1])
tags = sys.argv[2:]
source = urllib.urlopen(url)
soup = BeautifulSoup(source, 'html.parser')
if '-u' in tags:
	urls(soup)
if '-i' in tags:
	images(soup)