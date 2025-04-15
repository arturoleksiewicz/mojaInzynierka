import requests
from requests.auth import HTTPBasicAuth


class CensysFetcher:
    def __init__(self, uid, secret):
        self.uid = uid
        self.secret = secret

    def get_host_data(self, company_name):
        company_domain = f"{company_name.lower()}.com"

        url = "https://search.censys.io/api/v2/hosts/search"
        headers = {"accept": "application/json"}
        params = {
            "q": company_domain,
            "per_page": 50,
            "virtual_hosts": "EXCLUDE",
            "sort": "RELEVANCE"
        }

        response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(self.uid, self.secret))

        if response.status_code == 200:
            data = response.json()
            hits = data.get('result', {}).get('hits', [])
            host_data = []
            for result in hits:
                ip = result.get('ip', 'N/A')
                port = result.get('services', [{}])[0].get('port', 'N/A')
                organization = result.get('autonomous_system', {}).get('description', 'N/A')
                last_checked = result.get('last_updated_at', 'N/A')
                location = result.get('location', {})
                operating_system = result.get('operating_system', {}).get('product', 'N/A')

                host_data.append({
                    "IP": ip,
                    "Port": port,
                    "Organization": organization,
                    "Last Checked": last_checked,
                    "Country": location.get('country', 'N/A'),
                    "City": location.get('city', 'N/A'),
                    "Latitude": location.get('coordinates', {}).get('latitude', 'N/A'),
                    "Longitude": location.get('coordinates', {}).get('longitude', 'N/A'),
                    "Operating System": operating_system,
                    "Hostnames": result.get('hostnames', []),
                    "Domains": result.get('domains', [])
                })
            return host_data
        else:
            print("Error fetching data from Censys:", response.status_code, response.text)
            return []
