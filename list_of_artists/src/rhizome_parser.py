# fetch the list of artists in rhizome: https://artbase.rhizome.org/wiki/Browse/by_artist_name
# list is saved in artistsrhizome.txt

import requests
from bs4 import BeautifulSoup

# this page has the list of artists names
response = requests.get('https://artbase.rhizome.org/wiki/Browse/by_artist_name')
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
artistslist = open('artistsrhizome.txt', 'w')

if response.ok:
    # fetch all the <li> elements
    headers = soup.find_all('li')
    for header in headers:
    	# remove the number of occurences that is in () after the name
        parts=header.text.split('(')
    	# save the artist name in file
        artistslist.write(parts[0]+'\n')
        artistslist.close()
else:
    print ("Boo! {}".format(response.status_code))
    print (response.text)
