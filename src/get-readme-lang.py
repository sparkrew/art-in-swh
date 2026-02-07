import fasttext
from huggingface_hub import hf_hub_download
import os
import json

# expects a GHdatafile JSON file, which should be an array of JSON objects similar to the example found in sample-rq2-data.json
def getReadmeLang(GHdatafile):
    # download model and get the model path
    # cache_dir is the path to the folder where the downloaded model will be stored/cached.
    model_path = hf_hub_download(repo_id="cis-lmu/glotlid", filename="model_v3.bin", cache_dir=None)
    print("model path:", model_path)
    # load the model
    model = fasttext.load_model(model_path)
    filename=GHdatafile.split(".json")
    destfilename=filename[0]+"_with_language.json"
    os.system(f"cp {GHdatafile} {destfilename}")
    with open(GHdatafile, 'r') as file:
        GHdata = json.load(file)
    for repo in GHdata:
        if repo["readme"]:
            cleanreadme=repo["readme"].replace('\n', '')
            repo["readme-lang"]=model.predict(cleanreadme)[0]
            # lang=model.predict(cleanreadme,3)
            # print(lang[0])
        else:
            repo["readme-lang"]="no-lang"  
    with open(destfilename, 'w') as json_file:
        json.dump(GHdata, json_file)


def main():
    getReadmeLang("sample-rq2-datawith_locations.json")    

if __name__ == "__main__":
    main()
