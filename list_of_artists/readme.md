# Artist Names Collection

A curated repository of artist names from different parts of the world

### Overview
This project gathers artist names and information from the following sources:

- **re|thread digital art studio** - Curated list of algorithmic and generative artists
- **MoMA Collection** - Artists from The Museum of Modern Art, New York City, United States
- **MNBAC Collection** - Artists from Museo Nacional de Bellas Artes de Cuba, Havana, Cuba


### Data Sources
#### The Museum of Modern Art (MoMA)

Location: New York City, United States
Source: MoMA Collection Repository
Output: MomaArtistNamesParsed.txt
Description: Comprehensive list of artists featured in MoMA's permanent collection

#### Museo Nacional de Bellas Artes (MNBA)

Location: Havana, Cuba
Source: MNBA Official Website
Description: Artists represented in Cuba's national fine arts museum collection

#### Generative Art Collection

Source: re|thread digital art studio's algorithmic art course
Output: ReThreadCuratedArtistList.txt
Origin: IFT 6251 Algorithmic Art course, University of Montreal (Prof. Benoit Baudry)
Repository: Algorithmic Art Course
Description: Curated selection of prominent generative and algorithmic artists

### Repository Structure
```
├── source_data/
│   ├── source_data_moma_artists.txt
├── src/
│   ├── mnbac_cuba_parser.py           # MoMA data extraction script
│   ├── moma_us_parser.py      # MNBA data extraction script
│── mnbac_cuba_artists.txt
│── moma_us_artists.txt
│── re-thread_curated_artists.txt
└── readme.md
```

In the `src` folder you will find the scripts used to retrieve the all the information.

- `moma_parser.py`: python script to parse and list the artists from MOMA, NY — `MomaArtistNamesParsed.txt`. The data is retrieved from the [Museum of Modern Art's collection repository](https://github.com/MuseumofModernArt/collection/blob/main/Artists.csv).

- `mnba_cuba_parser.py`: python script to parse and list the artists from the MNBA, Havana. The data is retrieved directly from their [website](https://www.bellasartes.co.cu/).

- Curated list of generative art artists — `ReThreadCuratedArtistList.txt`. Extracted from the IFT 6251 Algorithmic Art course from the University of Montreal, taught by Professor Benoit Baudry . The data was sourced from this [repository](https://github.com/rethread-studio/algorithmic-art-course).

### Scripts
`moma_parser.py`

Python script that processes `source_data_moma_artists.txt` file to extract and format artist names from their public collection repository.

`mnba_cuba_parser.py`

Web scraping script that retrieves artist information directly from the MNBA website, parsing their online collection.