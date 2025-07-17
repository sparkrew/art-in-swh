# fetch the list of artists in superrare: https://superrare.com/artists
# first manually scrapped the list in json from the web page
# then the script extracts the names and saves them in artistssuperrare.txt

import json
with open('superrareartists.json', 'r') as file:
    data = json.load(file)
artistslist = open('artistssuperrare.txt', 'w')
artistslist.write("# list of artists on the NFT platform superrare https://superrare.com/artists")

for artist in data:
    name =artist["fullName"]
    if name != "" and name!=None:
        artistslist.write(name+'\n')
        print(name)
