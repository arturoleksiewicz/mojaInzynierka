import requests
import pandas as pd

# Define your API key and the base URL
API_KEY = 'c424c0ad9ac6e150e15c4304a2cfd94f'
BASE_URL = 'https://api.crunchbase.com/api/v4/entities/organizations/'


# Function to get company data
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


# Function to display company data in a readable format
def display_company_data(data):
    # Wyodrębnij dane identyfikacyjne firmy
    identifier = data.get("properties", {}).get("identifier", {})

    # Przygotowanie informacji do wyświetlenia
    company_info = {
        "UUID": identifier.get("uuid", "N/A"),
        "Name": identifier.get("value", "N/A"),
        "Permalink": f"https://www.crunchbase.com/organization/{identifier.get('permalink', 'N/A')}",
        "Entity Definition": identifier.get("entity_def_id", "N/A"),
        "Image ID": identifier.get("image_id", "N/A"),
    }

    # Konwersja danych do DataFrame dla czytelności
    df = pd.DataFrame([company_info])

    print("\nCompany Identifier Data:\n")
    print(df.to_markdown(index=False))  # Wyświetla tabelę w konsoli


# Example usage
if __name__ == "__main__":
    company_slug = 'panasonic'  # Replace with the desired company slug
    company_data = get_company_data(company_slug)

    if company_data:
        display_company_data(company_data)
