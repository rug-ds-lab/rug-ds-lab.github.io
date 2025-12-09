"""
This module fetches bibliographic data from ORCID using the ORCID API.

It provides functions to retrieve member works and citations.
"""
import os
import sys
import time
import json
import requests
import re

import bibtexparser
from pylatexenc.latex2text import LatexNodes2Text

BASE_URL = "https://pub.orcid.org/v3.0/"


def remove_double_braces(text: str) -> str:
    # replace {{x}} with x (for any single char inside)
    return re.sub(r"\{\{([^\{\}])\}\}", r"\1", text)

def get_member_name(mem, key):
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
        response = requests.get(BASE_URL + mem + "/record", headers = headers, timeout = 10)
        response.raise_for_status()

        # Response succeeded
        data = response.json()
        return data['person']['name']["given-names"]['value'].lower() + "_" + data['person']['name']["family-name"]['value'].lower()


    except requests.exceptions.Timeout:
        print("Request timed out, no info returned")
        return ""

    except requests.exceptions.RequestException as e:
        print("Unable to connect to ORCID, no info returned")
        print("Error: " + str(e))
        return ""
    
def get_member_works(mem, key, rug_filter=False):
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

        if rug_filter:
            return [ws["put-code"] for g in data.get("group", []) for ws in g.get("work-summary", []) if ws["source"]["source-name"]["value"] == "University of Groningen"]
        else:
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
        result += [
            item['work']['citation']['citation-value']
            for item in data['bulk']
            if item.get('work') and item['work'].get('citation')
        ]

        # Limit to 10 requests per second
        if i + batch_size < len(putcodes):
            time.sleep(0.1)

    return result



def format_bibtex_entry(entry: str) -> str:
    try:
        bib_db = bibtexparser.loads(entry)
        if not bib_db.entries:
            return entry
        bib_entry = bib_db.entries[0]
        entry_type = bib_entry.get('ENTRYTYPE', 'article')
        entry_key = bib_entry.get('ID', 'unknown')
        text = ""
        for k, v in bib_entry.items():
            if k in ('ENTRYTYPE', 'ID'):
                continue
            
            v = re.sub(r'sub(\S*)\/sub', r'<sub>\1</sub>', v)
            v = LatexNodes2Text().latex_to_text(v)
            v = v.replace("\"", "").strip()
            text += f"{k} = \"{v}\",\n"
        return f"@{entry_type}{{{entry_key},\n{text.strip()[:-1]}\n}}\n"
    except Exception as e:
        print(f"Error processing entry: {entry}")
        return entry
    


if __name__ == "__main__":
    # Get the API key from ENV
    api_key = os.getenv("API_KEY")
    if api_key is None:
        sys.stderr.write("No API key provided. Exiting.\n")
        sys.exit()

    # Check if ./_bibliography/ exist
    os.makedirs(os.path.dirname("./_bibliography/"), exist_ok=True)

    # Load the member ID's
    with open('member_ids.txt', 'r', encoding='utf-8') as f:
        member_ids = [line.strip() for line in f]

    # Fetch citations for all members
    for member in member_ids:
        # Get the list of works from a member
        name = get_member_name(member, api_key)
        print(name)
        work_codes = get_member_works(member, api_key, rug_filter=True)
        citations = get_bibtex(member, "/works/", work_codes, api_key)
        txt_arr: list[str] = []

        for cite in citations:
            try:
                fixed_str = cite.encode("utf-8").decode("utf-8").encode("latin1").decode("utf-8")
            except (UnicodeDecodeError, UnicodeEncodeError):
                fixed_str = cite
            
            decoded = format_bibtex_entry(fixed_str)
            txt_arr.append(decoded)
        
        
        with open(f"./_bibliography/{name}.bib", "w", encoding="utf-8") as f:
            f.write("\n\n".join(txt_arr))

    sys.stdout.write("finish updating.\n")