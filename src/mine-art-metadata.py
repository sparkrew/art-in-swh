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
    
def get_user_info(username):
    # https://docs.github.com/en/graphql/reference/objects#user
    # this query expects a user login as a parameter and returns the location, date of creation and bio for that login
    query = """
    query getUserLocation($login: String!) {
      user(login: $login) {
        login
        location
        createdAt
        bio
      }
    }
    """

    request = requests.post(
        'https://api.github.com/graphql', 
        json={"query": query, "variables": {"login": username}},
        headers=headers)
    if request.status_code == 200:
        data = request.json()
        return data["data"]["user"]
        
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
        
def build_query_for_remaining_requests():
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
  return queryrate

def build_query_for_repos(repo_urls):
  #filename="../data/test-sample.json"
  search_query=""
  with open(repo_urls, 'r') as file:
      data = json.load(file)

  for i in data:
      search_query+="repo:"+i+" "

  # f""" at the start makes it an f-string, so a variable {s} is replaced by the variable’s value.
  # The outer GraphQL braces must be escaped with double braces {{ ... }} so that Python doesn’t treat them as placeholders.
  # Inside the query, the query: field expects a quoted string, so you wrap {s} in ".
  # The idea of search comes from https://til.simonwillison.net/github/bulk-repo-github-graphql
  # The following query searches a set of repos that in the search_query string
  # For each repo, it queries the name of the owner, date of creation, the number of commits, the top 100 contributors and the readme
  query = f"""
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
  return query


def print_repos_data(allrepos):
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
        userprofile = get_user_info(main_contributor)
        if len(userprofile)!=0:
            print(f"Location: {userprofile["location"]}")
            print(f"Bio: {userprofile["bio"]}")
            isReliable, textBytesFound, details = cld2.detect(userprofile["bio"])
            if isReliable : print(f"Languages of bio: {str(details)}")
            print(f"createdAt: {userprofile["createdAt"]}")
      else:
        print("Main contributor: no contributor is listed")
      readme = repo["object"]["text"] if repo["object"] else None
      print(readme)
      isReliable, textBytesFound, details = cld2.detect(readme)
      if isReliable : print(f"Languages of readme: {str(details)}")
      print("+++++++++++++++++++++++++++++++++++++")

def save_repos_data(allrepos):
  repos_matadata = []
  for repo in allrepos:
      onerepo=dict()
      onerepo["name"]=repo["nameWithOwner"]
      onerepo["creation_date"]=repo["createdAt"]
      commits = repo["defaultBranchRef"]["target"]["history"]["totalCount"]
      onerepo["nb_commits"] = commits
      contributors = [edge["node"]["author"]["user"]["login"]
                  for edge in repo["defaultBranchRef"]["target"]["history"]["edges"]
                  if edge["node"]["author"]["user"]]
      if len(contributors)!= 0:
        main_contributor = max(set(contributors), key=contributors.count)
        onerepo["main_contributor"]=main_contributor
        userprofile = get_user_info(main_contributor)
        profile=dict()
        if len(userprofile)!=0:
            profile["location"]=userprofile["location"] if userprofile["location"]!="" else "none"
            profile["bio"]=userprofile["bio"] if userprofile["bio"]!="" else "none"
        else:
            profile["location"]="none"
            profile["bio"]="none"
            print("no user profile for "+main_contributor)
      else:
          onerepo["main_contributor"]="none"         
          profile=dict()
          profile["location"]="none"
          profile["bio"]="none"
          print("no contributor for "+main_contributor)
      onerepo["main_contributor_profile"]=profile
          
      readme = repo["object"]["text"] if repo["object"] else None
      onerepo["readme"]=readme

      repos_matadata.append(onerepo)

  with open("repos_data.json", "w") as f:
    json.dump(repos_matadata, f)

def main():
  query_for_repositories=build_query_for_repos("../data/test-sample.json")
  result = run_query(query_for_repositories)
  allrepos = result["data"]["search"]["nodes"]
  #print_repos_data(allrepos)
  save_repos_data(allrepos)

if __name__ == "__main__":
    main()


      # queryrate=build_query_for_remaining_requests()
      # run_query(queryrate)
      # rateafter = run_query(queryrate)
      # total_hits = ratebefore["data"]["rateLimit"]["remaining"] - rateafter["data"]["rateLimit"]["remaining"]# Drill down the dictionary
      # print("Total requests - {}".format(total_hits)+". Was there before {}".format(ratebefore["data"]["rateLimit"]["remaining"])+", and now {}".format(rateafter["data"]["rateLimit"]["remaining"]))
