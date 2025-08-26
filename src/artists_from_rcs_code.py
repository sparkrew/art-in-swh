import requests
from bs4 import BeautifulSoup
import spacy
import pandas as pd
import re


def save_and_print(artist_names, file_name):
    # Save in .txt file and print the results
    with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
        for artist in sorted(artist_names):
            f.write(artist + "\n")

    print(f"{len(artist_names)} possible artist found and saved in '{file_name}.txt'")
    
def get_artists_case_1(soup):
    # Use web-scrapping only: Split the lines and look for the line with only the 'by' text, then the next line has the 
    # artists names
    # Possible problem here: Some artist are missing
    clean_text = soup.get_text(separator="\n", strip=True)
    lines = clean_text.splitlines()
    artist_list = []

    i = 0
    while i < len(lines):
         # Every time he finds a 'by' line => the next one will be the artists line
        if lines[i].strip().lower() == "by":
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                parts = re.split(r",| and ", next_line)
                # Remove spaces
                artist_list.extend([p.strip() for p in parts if p.strip()])
            i += 2
        else:
            i += 1

    # Remove duplicates and order the list
    artist_names = sorted(set(artist_list))
    return artist_names
    
    
def get_artist_case_2(nlp, soup):
    # Use web-scrapping and nlp: Split the text by '\n' and every sentence will be procede by the nlp
    # then, I take the PERSON entities.
    # Possible problem here: The method will returns false positives- the model labels some as PERSON entities when they are not;
    # and it returns false negatives- people who are assigned to another entity type
    clean_text = soup.get_text(separator="\n", strip=True)
    lines = clean_text.splitlines()
    artist_names = set()

    for text in lines:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                artist_names.add(ent.text )

    return artist_names

def union_method(result1, result2):
    output_file_name = "artists_from_rcs.txt"

    # Join sets
    artist_names = set(result1) | set(result2)

    # Save
    with open(output_file_name, "w", encoding="utf-8") as f:
        for name in sorted(artist_names):
            f.write(name + "\n")

    print(f"Completed join. Generated file: {output_file_name}")

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    url = "https://www.rightclicksave.com/articles"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    #file_list = ["artists_from_rcs_case_1", "artists_from_rcs_case_2"]
    
    # Case 1
    result1 = get_artists_case_1(soup)
    #save_and_print(result1, file_list[0])
    
    # Case 2
    result2 = get_artist_case_2(nlp, soup)
    #save_and_print(result2, file_list[1])
    
    # Join files
    union_method(result1, result2)