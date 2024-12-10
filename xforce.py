import requests


# Funkcja pobierająca informacje o zagrożeniach dla danej firmy
def get_threat_intel_for_company(company_name, api_key):
    url = f"https://api.xforce.ibmcloud.com/api/threat-intel/search?q={company_name}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Przykładowe wypisanie wyników
        if 'rows' in data:
            print(f"Zagrożenia dla firmy {company_name}:")
            for threat in data['rows']:
                print(f"- Typ zagrożenia: {threat['type']}")
                print(f"  Opis: {threat['description']}")
                print(f"  Poziom ryzyka: {threat['risk_score']}")
                print(f"  Data publikacji: {threat['created']}")
        else:
            print("Brak zagrożeń dla tej firmy w bazie IBM X-Force.")
    else:
        print("Błąd podczas pobierania danych:", response.status_code)


# Przykładowe użycie funkcji
company_name = "example_company"
api_key = "your_ibm_xforce_api_key"
get_threat_intel_for_company(company_name, api_key)
