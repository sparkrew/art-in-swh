import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bellasartes.co.cu"
ARTISTAS_URL = f"{BASE_URL}/artistas"

def get_artist_names_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    artist_divs = soup.find_all("div", class_="views-field views-field-name")
    artist_names = [div.get_text(strip=True) for div in artist_divs if div.get_text(strip=True)]
    
    return artist_names

def main():
    all_artists = []
    page = 0

    while True:
        paged_url = f"{ARTISTAS_URL}?page={page}"
        artist_names = get_artist_names_from_page(paged_url)

        if not artist_names:
            break  # Exit when no more artists are found
        print(f"Page {page + 1}: Retrieved {len(artist_names)} artists.")
        all_artists.extend(artist_names)
        page += 1

    with open('../mnba_cuba_artists.txt', 'x') as output_f:  
        for name in all_artists:
            output_f.write(name + '\n')

if __name__ == "__main__":
    main()
