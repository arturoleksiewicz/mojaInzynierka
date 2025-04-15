import requests
import os
import json
from bs4 import BeautifulSoup


def download_html_files(urls, output_folder):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_map = {}
    for url in urls:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            file_name = url.split("//")[-1].replace("/", "_").replace(".", "_") + ".html"
            file_path = os.path.join(output_folder, file_name)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)

            file_map[url] = file_path
            print(f"Pobrano i zapisano plik z {url}: {file_path}")
        except Exception as e:
            print(f"Błąd podczas pobierania {url}: {e}")

    return file_map


def fetch_trustpilot_data_from_html(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        script_tag = soup.find("script", type="application/ld+json")
        if script_tag:
            data = json.loads(script_tag.string)

            if '@graph' in data:
                for item in data['@graph']:
                    if item.get('@type') == 'LocalBusiness' and 'aggregateRating' in item:
                        rating_data = item['aggregateRating']
                        return {
                            'review_count': rating_data.get("reviewCount", "N/A"),
                            'average_score': rating_data.get("ratingValue", "N/A"),
                        }

        return {'review_count': 'N/A', 'average_score': 'N/A'}

    except Exception as e:
        print(f"Błąd podczas przetwarzania pliku {file_path}: {e}")
        return {'review_count': 'N/A', 'average_score': 'N/A'}


def clean_up_files(file_paths):
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Usunięto plik: {file_path}")
        except Exception as e:
            print(f"Błąd podczas usuwania pliku {file_path}: {e}")

