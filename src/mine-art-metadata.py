import os
import requests
import json
import pycld2 as cld2
from dotenv import load_dotenv # type: ignore

load_dotenv()
headers = {"Authorization": "Bearer "+os.getenv("API_KEY")}


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    
    request = requests.post(
        'https://api.github.com/graphql', 
        json={'query': query}, 
        headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    
def get_user_location(username):
    request = requests.post(
        'https://api.github.com/graphql', 
        json={"query": queryforuser, "variables": {"login": username}},
        headers=headers)
    if request.status_code == 200:
        data = request.json()
        return data["data"]["user"]
        
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
queryrate = """
{
  viewer {
    login
  }
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
}
"""


filename="../data/test-sample.json"
search_query=""
with open(filename, 'r') as file:
    data = json.load(file)

for i in data:
    search_query+="repo:"+i+" "

# f""" at the start makes it an f-string, so a variable {s} is replaced by the variable’s value.
# The outer GraphQL braces must be escaped with double braces {{ ... }} so that Python doesn’t treat them as placeholders.
# Inside the query, the query: field expects a quoted string, so you wrap {s} in ".
# The idea of search comes from https://til.simonwillison.net/github/bulk-repo-github-graphql
# The following query searches a set of repos that in the search_query string
# For each repo, it queries the name of the owner, date of creation, the number of commits, the top 100 contributors and the readme
queryforrepositories = f"""
{{
  search(type: REPOSITORY, query: "{search_query}", first: 100) {{
    nodes {{
      ... on Repository {{
        nameWithOwner
        createdAt
        
        # Contributors (commit authors)
        defaultBranchRef {{
          name
          target {{
            ... on Commit {{
              history(first: 100) {{
                totalCount   # total commits (capped if large)
                edges {{
                  node {{
                    author {{
                      user {{
                        login
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
 
        # README content (if exists)
        object(expression: "HEAD:README.md") {{
          ... on Blob {{
            text
          }}
        }}
      }}
    }}
  }}
}}
"""

# https://docs.github.com/en/graphql/reference/objects#user
# this query expects a user login as a parameter and returns the location, date of creation and bio for that login
queryforuser = """
query getUserLocation($login: String!) {
  user(login: $login) {
    login
    location
    createdAt
    bio
  }
}
"""

#ratebefore = run_query(queryrate)

result = run_query(queryforrepositories)
allrepos = result["data"]["search"]["nodes"]
for repo in allrepos:
    name=repo["nameWithOwner"]
    print(name)
    print("+++++++++++++++++++++++++++++++++++++")
    date=repo["createdAt"]
    print(f"Created on: {date}")
    commits = repo["defaultBranchRef"]["target"]["history"]["totalCount"]
    print(f"Number of commits: {commits}")
    contributors = [edge["node"]["author"]["user"]["login"]
                for edge in repo["defaultBranchRef"]["target"]["history"]["edges"]
                if edge["node"]["author"]["user"]]
    if len(contributors)!= 0:
      main_contributor = max(set(contributors), key=contributors.count)
      print(f"Main contributor: {main_contributor}")
      loc=get_user_location(main_contributor)
      if len(loc)!=0:
          print(f"Location: {loc["location"]}")
          print(f"Bio: {loc["bio"]}")
          isReliable, textBytesFound, details = cld2.detect(loc["bio"])
          if isReliable : print(f"Languages of bio: {str(details)}")
          print(f"createdAt: {loc["createdAt"]}")
    else:
      print("Main contributor: no contributor is listed")
    # file_count = len(repo["object(expression: \"HEAD:\")"]["entries"])
    # print(f"Number of files in root: {file_count}")
    # file_count = len(repo["object(expression: \"HEAD:\")"]["entries"])
    # print("Number of files at root: "+file_count)
    readme = repo["object"]["text"] if repo["object"] else None
    print(readme)
    isReliable, textBytesFound, details = cld2.detect(readme)
    if isReliable : print(f"Languages of readme: {str(details)}")
    print("+++++++++++++++++++++++++++++++++++++")


    # rateafter = run_query(queryrate)
    # total_hits = ratebefore["data"]["rateLimit"]["remaining"] - rateafter["data"]["rateLimit"]["remaining"]# Drill down the dictionary
    # print("Total requests - {}".format(total_hits)+". Was there before {}".format(ratebefore["data"]["rateLimit"]["remaining"])+", and now {}".format(rateafter["data"]["rateLimit"]["remaining"]))
