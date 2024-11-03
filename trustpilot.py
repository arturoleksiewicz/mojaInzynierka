import requests
from bs4 import BeautifulSoup

class TrustpilotFetcher:
    def search_trustpilot(self, company_name):
        query = f"{company_name} site:trustpilot.com"
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Failed to retrieve search results. Status code: {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        for g in soup.find_all('div', class_='g'):
            title = g.find('h3')
            if title:
                title_text = title.get_text()
                link = g.find('a')['href']
                search_results.append((title_text, link))

        detailed_results = []
        for title, link in search_results:
            reviews = self.fetch_reviews(link, headers)
            detailed_results.append((title, link, reviews))

        return detailed_results

    def fetch_reviews(self, url, headers):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return f"Failed to retrieve page content. Status code: {response.status_code}"
            page_soup = BeautifulSoup(response.text, 'html.parser')
            reviews = []
            review_elements = page_soup.find_all('div', {'class': 'styles_reviewContent__fhKmk'})
            for review in review_elements:
                review_text = review.find('p', {'class': 'styles_reviewContent__text__jv1zt'})
                if review_text:
                    reviews.append(review_text.get_text(separator="\n", strip=True))
            return reviews
        except Exception as e:
            return f"An error occurred: {e}"
