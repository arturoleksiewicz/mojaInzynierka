import requests

def hackertarget_tool(option, target):
    base_url = "https://api.hackertarget.com"
    endpoints = {
        "hostsearch": "/hostsearch/",
        "dnslookup": "/dnslookup/",
        "geoip": "/geoip/",
        "reversedns": "/reversedns/"
    }

    if option not in endpoints:
        return f"Nieprawidłowa opcja: {option}"

    url = f"{base_url}{endpoints[option]}?q={target}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text
            if "error" in data.lower():
                return f"Błąd: {data}"
            else:
                return data
        else:
            return f"Błąd połączenia z API. Kod statusu: {response.status_code}"
    except Exception as e:
        return f"Wystąpił błąd: {e}"

class HackerTargetFetcher:
    def run_all_hackertarget_functions(self, company_name):
        target_domain = f"{company_name.lower()}.com"  # Przyjmuje, że domena to nazwa_firmy.com

        functions = [
            "hostsearch", "nmap", "traceroute", "ping",
            "dnslookup", "whois", "geoip", "reversedns"
        ]

        results = {}
        for function in functions:
            result = hackertarget_tool(function, target_domain)
            results[function] = result

        return results
