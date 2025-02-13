"""
This module fetches bibliographic data from ORCID using the ORCID API.

It provides functions to retrieve member works and citations.
"""
import os
import sys
import time
import json
import requests

BASE_URL = "https://pub.orcid.org/v3.0/"

def get_member_works(mem, key):
    """
    Fetch the list of work put codes for a given ORCID member.

    :param mem: ORCID member ID
    :return: list of put codes
    """
    headers = {
        "Authorization": "Bearer" + key,
        "Content-Type": "application/orcid+json"
    }

    try:
        response = requests.get(BASE_URL + mem + "/works", headers = headers, timeout = 10)
        response.raise_for_status()

        # Response succeeded
        data = response.json()
        return [ws["put-code"] for g in data.get("group", []) for ws in g.get("work-summary", [])]

    except requests.exceptions.Timeout:
        print("Request timed out, no info returned")
        return ""

    except requests.exceptions.RequestException as e:
        print("Unable to connect to ORCID, no info returned")
        print("Error: " + str(e))
        return ""

def get_bibtex(uid, endpoint, putcodes, key, batch_size=100):
    """
    Fetch bibtex entries from ORCID API in batches.

    :param id: ORCID member ID
    :param endpoint: endpoint to query, e.g. "/works/"
    :param putcodes: list of put codes to query
    :param batch_size: number of put codes to query at once
    :return: list of bibtex entries
    """
    headers = {
        "Authorization": "Bearer" + key,
        "Content-Type": "application/vnd.orcid+json"
    }

    result = []

    for i in range(0, len(putcodes), batch_size):
        batch = putcodes[i:i+batch_size]

        work_url = BASE_URL + uid + endpoint + ",".join(map(str, batch))
        response = requests.get(url=work_url, headers = headers, timeout = 10)

        if not response.ok:
            sys.stderr.write("Error fetching bibtex batch for ", uid)
            sys.exit()

        # Parse the data
        data = response.json()

        results += [
            item['work']['citation']['citation-value']
            for item in data['bulk']
            if item.get('work') and item['work'].get('citation')
        ]

        # Limit to 10 requests per second
        if i + batch_size < len(putcodes):
            time.sleep(0.1)

    return result

if __name__ == "__main__":
    # Get the API key from ENV
    api_key = os.getenv("API_KEY")
    if api_key is None:
        sys.stderr.write("No API key provided. Exiting.\n")
        sys.exit()

    # Load the member ID's
    with open('member_ids.txt', 'r', encoding='utf-8') as f:
        member_ids = [line.strip() for line in f]

    # Fetch citations for all members
    for member in member_ids:
        # Get the list of works from a member
        work_codes = get_member_works(member, api_key)
        citations = get_bibtex(member, "/works/", work_codes, api_key)

        with open("citations.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(citations, indent = 4))
