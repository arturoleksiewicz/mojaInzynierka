import requests
import pandas as pd
import os

API_KEY = os.getenv("crunch")
BASE_URL = 'https://api.crunchbase.com/api/v4/entities/organizations/'


def get_company_data(company_slug):
    url = f"{BASE_URL}{company_slug}?user_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def display_company_data(data):
    identifier = data.get("properties", {}).get("identifier", {})

    company_info = {
        "UUID": identifier.get("uuid", "N/A"),
        "Name": identifier.get("value", "N/A"),
        "Permalink": f"https://www.crunchbase.com/organization/{identifier.get('permalink', 'N/A')}",
        "Entity Definition": identifier.get("entity_def_id", "N/A"),
        "Image ID": identifier.get("image_id", "N/A"),
    }

    df = pd.DataFrame([company_info])

    print("\nCompany Identifier Data:\n")
    print(df.to_markdown(index=False))


# Example usage
if __name__ == "__main__":
    company_slug = 'panasonic'
    company_data = get_company_data(company_slug)

    if company_data:
        display_company_data(company_data)
