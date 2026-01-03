import requests
import os
import time
import json
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv # type: ignore

load_dotenv()
# Your Geoapify API key
apiKey = os.getenv("API_KEY_GEO")
# Time to wait between attempts (in seconds)
timeout = 1
# How many times to try checking the results
maxAttempts = 7


# code for geocode_batch and fetch_results found here: https://www.geoapify.com/tutorial/batch-geocoding-python/

# expects one String unstructured address
# returns a json array with a single geoapi object for the address
def geocode(address):
    url = f"https://api.geoapify.com/v1/batch/geocode/search?apiKey={apiKey}"
    response = requests.post(url, json=[address])

    if response.status_code != 202:
        print("Failed to create the job. Check the input data.")
        return

    jobId = response.json()["id"]
    results_url = f"{url}&id={jobId}"
    print(f"Job submitted. Waiting for results (Job ID: {jobId})...")

    time.sleep(timeout)
    return fetch_results(results_url, attempt=0)

# expects an array of Strings unstructured addresses
# returns an array of json geoapi objects, one per address
def geocode_batch(addresses):
    # Send a batch geocoding job
    url = f"https://api.geoapify.com/v1/batch/geocode/search?apiKey={apiKey}"
    response = requests.post(url, json=addresses)

    if response.status_code != 202:
        print("Failed to create the job. Check the input data.")
        return

    jobId = response.json()["id"]
    results_url = f"{url}&id={jobId}"
    print(f"Job submitted. Waiting for results (Job ID: {jobId})...")

    time.sleep(timeout)
    return fetch_results(results_url, attempt=0)

def fetch_results(url, attempt):
    # Poll for job results
    response = requests.get(url)

    if response.status_code == 200:
        print("Job completed.")
        return response.json()
    elif response.status_code == 202 and attempt < maxAttempts:
        print(f"Still processing... (Attempt {attempt + 1})")
        time.sleep(timeout)
        return fetch_results(url, attempt + 1)
    else:
        print("Results not ready. You can check later at:")
        print(url)
        print(response.json())
        return response.json()

# expects a GHdatafile JSON file, which should be an array of JSON objects similar to the example found in sample.json
def getGHloc(GHdatafile):
    filename=GHdatafile.split(".json")
    destfilename=filename[0]+"with_locations.json"
    os.system(f"cp {GHdatafile} {destfilename}")
    with open(GHdatafile, 'r') as file:
        GHdata = json.load(file)
    # for every object in the file, add fields location_normalized, location_type, location_lat, location_lon
    # if the object's "location" is "none", then all fields are set to "none"
    # if the request times out, then all fields are set to time-out. These objects can be queried again later
    # if geoapi returns a response that does not have a "result_type" field, then all fields are set to "not_found"
    # if the the geoapi response has a "result_type", we filter the main ones (country, city, etc.) and set location_type and location_normalized accordingly
    # if lon is available, we set location_lat, location_lon
    for repo in GHdata:
        if repo["main_contributor_profile"]["location"]!="none":
            loc=geocode(repo["main_contributor_profile"]["location"])
            if "status" in loc:
                repo["main_contributor_profile"]["location_normalized"]="time-out"
                repo["main_contributor_profile"]["location_type"]="time-out"
                repo["main_contributor_profile"]["location_lat"]="time-out"
                repo["main_contributor_profile"]["location_lon"]="time-out"
            else:
                if "result_type" in loc[0]:
                    repo["main_contributor_profile"]["location_type"]=loc[0]["result_type"]
                    if loc[0]["result_type"] == "city":
                        repo["main_contributor_profile"]["location_normalized"]=loc[0]["city"]
                    elif loc[0]["result_type"] == "country":
                        repo["main_contributor_profile"]["location_normalized"]=loc[0]["country"]
                    elif loc[0]["result_type"] == "state":
                        repo["main_contributor_profile"]["location_normalized"]=loc[0]["formatted"]
                    elif loc[0]["result_type"] == "county":
                        repo["main_contributor_profile"]["location_normalized"]=loc[0]["formatted"]
                    elif loc[0]["result_type"] == "district":
                        repo["main_contributor_profile"]["location_normalized"]=loc[0]["formatted"]
                    elif loc[0]["result_type"] == "state":
                        repo["main_contributor_profile"]["location_normalized"]=loc[0]["formatted"]
                    else:
                        repo["main_contributor_profile"]["location_normalized"]="not_found"
                else:
                    repo["main_contributor_profile"]["location_normalized"]="not_found"
                    repo["main_contributor_profile"]["location_type"]="not_found"
                    repo["main_contributor_profile"]["location_lat"]="not_found"
                    repo["main_contributor_profile"]["location_lon"]="not_found"
                if "lon" in loc[0]:
                    repo["main_contributor_profile"]["location_lat"]=loc[0]["lat"]
                    repo["main_contributor_profile"]["location_lon"]=loc[0]["lon"]
        else:
            repo["main_contributor_profile"]["location_normalized"]="none"
            repo["main_contributor_profile"]["location_type"]="none"
            repo["main_contributor_profile"]["location_lat"]="none"
            repo["main_contributor_profile"]["location_lon"]="none"
    with open(destfilename, 'w') as json_file:
        json.dump(GHdata, json_file)

# gets the self-declared Github user locations from the filename.json file passed as argument
# creates a copy of the file named filenamewith_locations.json
# searches each location with the [Geoapify](https://www.geoapify.com/) geocoding API
# saves the results of the search into filenamewith_locations.json
def main():
    getGHloc("sample-large.json")    

if __name__ == "__main__":
    main()

