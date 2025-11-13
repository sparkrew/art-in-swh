import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
headers = {"Authorization": "Bearer "+os.getenv("API_KEY")}


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
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
query2 = f"""
{{
  search(type: REPOSITORY, query: "{search_query}", first: 100) {{
    nodes {{
      ... on Repository {{
        nameWithOwner
        createdAt
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

# result_rate = run_query(queryrate)
# remaining_rate_limit = result_rate["data"]["rateLimit"]["remaining"] # Drill down the dictionary
# print("Remaining rate limit - {}".format(remaining_rate_limit))

result = run_query(query2) # Execute the query
rel = result["data"]["search"]["nodes"]
for repo in rel:
    name=repo["nameWithOwner"]
    print(name)
    print("+++++++++++++++++++++++++++++++++++++")
    date=repo["createdAt"]
    print(f"Created on {date}")
    # file_count = len(repo["object(expression: \"HEAD:\")"]["entries"])
    # print("Number of files at root: "+file_count)
    readme = repo["object"]["text"] if repo["object"] else None
    print(readme)
    print("+++++++++++++++++++++++++++++++++++++")

