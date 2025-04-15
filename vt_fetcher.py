import requests
import base64
from datetime import datetime  # Import modułu datetime


class VirusTotalFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def check_website_in_virustotal(self, company_name):
        url = f"https://{company_name}.com"

        virustotal_url = "https://www.virustotal.com/api/v3/urls"

        encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        headers = {
            "x-apikey": self.api_key
        }
        response = requests.get(f"{virustotal_url}/{encoded_url}", headers=headers)

        if response.status_code == 200:
            data = response.json()
            scan_timestamp = data.get("data", {}).get("attributes", {}).get("last_analysis_date", None)
            if scan_timestamp:
                scan_date = datetime.utcfromtimestamp(scan_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            else:
                scan_date = "Data not available"

            scan_data = {
                "URL": url,
                "Harmless": data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("harmless",
                                                                                                          "Data not available"),
                "Malicious": data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious",
                                                                                                           "Data not available"),
                "Suspicious": data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get(
                    "suspicious", "Data not available"),
                "Undetected": data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get(
                    "undetected", "Data not available"),
                "Scan Date": scan_date
            }
            return scan_data
        else:
            return {
                "Error": f"Nie udało się sprawdzić strony {url}. Kod odpowiedzi: {response.status_code}",
                "Details": response.text
            }
