import os
import sys
import time
import requests
import json

url_base = "https://pub.orcid.org/v3.0/"

api_key = os.getenv("API_KEY")

if api_key is None:
    sys.stderr.write("No API key provided. Exiting.\n")
    sys.exit()

# Load the member ID's
with open('member_ids.txt') as f:
    member_ids = [line.strip() for line in f]

def get_member_works(member):
    headers = {
        "Authorization": "Bearer" + api_key,
        "Content-Type": "application/orcid+json"
    }

    response = requests.get(url_base + member + "/works", headers = headers)

    if (response.ok):
        # Response success
        data = response.json()
        work_codes = [ws["put-code"] for g in data.get("group", []) for ws in g.get("work-summary", [])]
    
        return work_codes

    else:
        print("Request failed, no info returned")
        return ""
   
def get_bibtex(id, endpoint, putcodes, batch_size=100):
    headers = {
        "Authorization": "Bearer" + api_key,
        "Content-Type": "application/vnd.orcid+json"
    }
    
    result = []

    for i in range(0, len(putcodes), batch_size):
        batch = putcodes[i:i+batch_size]
        
        response = requests.get(url=url_base + id + endpoint + ",".join(map(str, batch)), headers = headers)

        if (not response.ok):
            sys.stderr.write("Error fetching bibtex batch for ", id)
            sys.exit()
        
        # Parse the data 
        data = response.json()
        
        citations = [
            item['work']['citation']['citation-value'] 
            for item in data['bulk'] 
            if item.get('work') and item['work'].get('citation') 
        ]

        result += citations

        if i + batch_size < len(putcodes):
            time.sleep(0.1)

    return result

if __name__ == "__main__":
    for member in member_ids:

        # Get the list of works from a member
        work_codes = get_member_works(member)
        citations = get_bibtex(member, "/works/", work_codes) 

        with open("citations.json", "w") as f:
            f.write(json.dumps(citations, indent = 4))
