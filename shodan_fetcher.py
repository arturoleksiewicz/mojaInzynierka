import shodan
import socket


class ShodanFetcher:
    def __init__(self, api_key):
        self.api = shodan.Shodan(api_key)

    def fetch_shodan_info(self, company_name):
        # Convert company name to lowercase and append ".com" to form the domain
        domain = f"{company_name.lower()}.com"

        try:
            # Resolve the IP address for the generated domain
            ip_address = socket.gethostbyname(domain)
            info = self.api.host(ip_address)

            # Extract and structure extended Shodan data
            shodan_data = {
                "IP": info.get('ip_str', 'Data not available'),
                "Country": info.get('country_name', 'Data not available'),
                "City": info.get('city', 'Data not available'),
                "Region Code": info.get('region_code', 'Data not available'),
                "Postal Code": info.get('postal_code', 'Data not available'),
                "Latitude": info.get('latitude', 'Data not available'),
                "Longitude": info.get('longitude', 'Data not available'),
                "ISP": info.get('isp', 'Data not available'),
                "ASN": info.get('asn', 'Data not available'),
                "Organization": info.get('org', 'Data not available'),
                "OS": info.get('os', 'Data not available'),
                "Last Update": info.get('last_update', 'Data not available'),
                "Tags": info.get('tags', []),
                "Domains": info.get('domains', []),
                "Hostnames": info.get('hostnames', []),
                "Vulnerabilities": [
                    {"CVE": vuln, "Summary": info['vulns'][vuln].get('summary', 'No summary available')}
                    for vuln in info.get('vulns', [])
                ],
                "Open Ports": []
            }

            # Collect detailed service information for each open port
            for service in info.get('data', []):
                port_info = {
                    "Port": service.get('port', 'Data not available'),
                    "Service": service.get('product', 'Data not available'),
                    "Version": service.get('version', 'Data not available'),
                    "Transport": service.get('transport', 'Data not available'),
                    "Banner": service.get('data', 'Data not available'),
                    "HTTP Headers": service.get('http', {}).get('headers', 'No HTTP headers available'),
                    "SSL Certificate": service.get('ssl', {}).get('cert', 'No SSL certificate data'),
                    "SSL Issuer": service.get('ssl', {}).get('issuer', 'No SSL issuer data'),
                    "SSL Expiration Date": service.get('ssl', {}).get('cert', {}).get('expires', 'Data not available')
                }
                shodan_data["Open Ports"].append(port_info)

            return shodan_data

        except shodan.APIError as e:
            print(f"An error occurred: {e}")
            return {"Error": str(e)}
        except socket.gaierror:
            print("Failed to resolve IP address for the given domain.")
            return {"Error": "Failed to resolve IP address for the given domain."}
