# fetch the list of artists in rhizome: https://artbase.rhizome.org/wiki/Browse/by_artist_name
# list is saved in artistsrhizome.txt

import requests
from bs4 import BeautifulSoup

# this page has the list of artists names
url='https://toledomuseum.org/exhibitions/infinite-images-the-art-of-algorithms'
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
artistslist = open('artiststoledo.txt', 'w')
artistslist.write("# list of artists exhibited at the Infinite Images: The Art of Algorithms exhbition, Toledo, OH, 2025: "+url)
if response.ok:
    # fetch all the <li> elements
    headers = soup.find_all('h4')
    for header in headers:
        parts=header.text.split('>')
    	# save the artist name in file
        artistslist.write(parts[0]+'\n')
    artistslist.close()
else:
    print ("Boo! {}".format(response.status_code))
    print (response.text)
