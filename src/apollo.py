import http.client
import json

# Set your Apollo API key here
API_KEY = "IOBtzah731A1o_UEXJ4MTw"

def fetch_email_by_person_id(person_id, person_name, organization_name, api_key):
    """
    Fetches (unlocks) the email for a specific person using Apollo's People Enrichment endpoint.
    This endpoint is a POST call to:
        https://api.apollo.io/api/v1/people/match
    You must supply sufficient identifying information (e.g. id, name, organization)
    and set reveal_personal_emails to True to request personal emails.
    
    Args:
        person_id (str): The Apollo person ID.
        person_name (str): The full name of the person.
        organization_name (str): The person's organization name.
        api_key (str): The Apollo API Key.
    
    Returns:
        str: The enriched email if available, or "No Email".
    """
    conn = http.client.HTTPSConnection("api.apollo.io")
    endpoint = "/api/v1/people/match"  # People Enrichment endpoint

    # Build the payload with the identifying information and set reveal_personal_emails to True
    payload = {
        "id": person_id,
        "name": person_name,
        "organization_name": organization_name,
        "reveal_personal_emails": True
    }
    payload_json = json.dumps(payload)

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'x-api-key': api_key,
    }

    try:
        conn.request("POST", endpoint, payload_json, headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        response_data = json.loads(data)
        # Debug: Print the full enrichment response
        print(f"Enrichment response for person ID {person_id}:")
        print(json.dumps(response_data, indent=4))
        # Extract the email from the nested "person" object
        return response_data.get("person", {}).get("email", "No Email")
    except Exception as e:
        print(f"Error fetching email for person ID {person_id}: {e}")
        return "No Email"
    finally:
        conn.close()


def fetch_people_by_company(api_endpoint, company_name, per_page=5, unlock_emails=False):
    """
    Fetch people data from Apollo API based on the given company name.
    
    Args:
        api_endpoint (str): Apollo API endpoint.
        company_name (str): Name of the company to search for.
        per_page (int): Number of results per page.
        unlock_emails (bool): If True, for people with locked/missing emails,
                              call the enrichment API to attempt unlocking.
    
    Returns:
        list: Sorted list of people with their details.
    """
    payload = json.dumps({
        "person_titles": [
            "CEO", "Founder", "Owner", "President",
            "Chief Marketing Director", "Chief Marketing Officer", "Chief Executive Director"
        ],
        "person_locations": ["United States"],
        "q_keywords": company_name,
        "company_revenue_min": 1000000,
        "per_page": per_page
    })

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'x-api-key': API_KEY,
    }

    conn = http.client.HTTPSConnection("api.apollo.io")

    try:
        print("Sending request with payload:")
        print(json.dumps(json.loads(payload), indent=4))

        conn.request("POST", api_endpoint, payload, headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')
        data = json.loads(data)

        if "people" in data and data["people"]:
            sorted_people = sorted(data['people'], key=lambda person: person['name'])
            formatted_results = []
            for person in sorted_people:
                # Get the email from the search results (it might be missing or locked)
                raw_email = person.get("email", "No Email")
                if unlock_emails and (raw_email == "No Email" or (isinstance(raw_email, str) and raw_email.startswith("email_not_unlocked"))):
                    # Call the enrichment endpoint to try to unlock the email
                    raw_email = fetch_email_by_person_id(
                        person["id"],
                        person["name"],
                        person.get('organization', {}).get('name', 'Unknown Company'),
                        API_KEY
                    )
                formatted_results.append({
                    "name": person['name'],
                    "title": person['title'],
                    "organization": person.get('organization', {}).get('name', 'Unknown Company'),
                    "email": raw_email
                })

            return formatted_results
        else:
            print(f"No results found for company: {company_name}")
            return []
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        conn.close()


def main():
    # Set your API endpoint for people search (this one has filters set as query parameters)
    API_ENDPOINT = ("/api/v1/mixed_people/search?"
                    "includedOrganizationKeywordFields%5B%5D=tags&"
                    "includedOrganizationKeywordFields%5B%5D=name&"
                    "revenueRange%5Bmin%5D=1000000&"
                    "company_keywords%5B%5D=CNC%2520Machines&"
                    "sortByField=%5Bnone%5D&"
                    "sortAscending=false&"
                    "personTitles%5B%5D=President&"
                    "personTitles%5B%5D=Owner&"
                    "personTitles%5B%5D=CMO&"
                    "personTitles%5B%5D=CEO&"
                    "personTitles%5B%5D=chiefmarketingofficer&"
                    "personTitles%5B%5D=chiefexecutiveofficer&"
                    "personTitles%5B%5D=chiefmarketingdirector&"
                    "personLocations%5B%5D=UnitedStates")

    company_name = input("Enter company name to search for: ").strip()
    per_page_input = input("Enter number of results per page (default 5): ").strip()
    per_page = int(per_page_input) if per_page_input.isdigit() else 5

    unlock_emails_input = input("Do you want to unlock emails using enrichment? (yes/no): ").strip().lower()
    unlock_emails = True if unlock_emails_input in ("yes", "y") else False

    results = fetch_people_by_company(API_ENDPOINT, company_name, per_page, unlock_emails)
    print(f"Fetched data for {company_name}:")
    print(results)

if __name__ == "__main__":
    main()
