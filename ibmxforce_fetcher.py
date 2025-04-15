import requests
from bs4 import BeautifulSoup


def search_threats_google(company_name):
    query = f"{company_name} site:exchange.xforce.ibmcloud.com"
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Błąd przy połączeniu z Google")
        return
    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all('div', class_='g')

    for result in search_results[:5]:
        title = result.find("h3")
        description = result.find("span", class_="aCOpRe")
        link = result.find("a")["href"]

        if title and description and link:
            print("Tytuł:", title.text)
            print("Opis:", description.text)
            print("Link:", link)
            print("-" * 80)


if __name__ == "__main__":
    company_name = "Google"
    search_threats_google(company_name)
