import requests
import os
import json
from bs4 import BeautifulSoup


def download_html_files(urls, output_folder):
    """
    Pobiera pliki HTML z podanych linków i zapisuje je lokalnie.

    Args:
        urls (list): Lista URL-i do stron, które mają zostać pobrane.
        output_folder (str): Ścieżka do folderu, w którym pliki zostaną zapisane.

    Returns:
        dict: Słownik, gdzie kluczami są URL-e, a wartościami ścieżki do pobranych plików.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_map = {}
    for url in urls:
        try:
            # Pobranie zawartości strony
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()

            # Generowanie nazwy pliku
            file_name = url.split("//")[-1].replace("/", "_").replace(".", "_") + ".html"
            file_path = os.path.join(output_folder, file_name)

            # Zapisanie pliku
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)

            file_map[url] = file_path
            print(f"Pobrano i zapisano plik z {url}: {file_path}")
        except Exception as e:
            print(f"Błąd podczas pobierania {url}: {e}")

    return file_map


def fetch_trustpilot_data_from_html(file_path):
    """
    Pobiera dane z lokalnego pliku HTML i wyciąga informacje o liczbie opinii oraz średniej ocenie.

    Args:
        file_path (str): Ścieżka do pliku HTML.

    Returns:
        dict: Słownik zawierający dane o liczbie opinii i średniej ocenie.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Szukanie JSON-LD
        script_tag = soup.find("script", type="application/ld+json")
        if script_tag:
            data = json.loads(script_tag.string)

            # Przeszukiwanie sekcji @graph
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
    """
    Usuwa podane pliki.

    Args:
        file_paths (list): Lista ścieżek do plików, które mają zostać usunięte.
    """
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Usunięto plik: {file_path}")
        except Exception as e:
            print(f"Błąd podczas usuwania pliku {file_path}: {e}")


def main():
    # Lista URL-i do pobrania
    urls = [
        "https://www.trustpilot.com/review/www.panasonic.com",
        "https://www.trustpilot.com/review/shop.panasonic.it",
    ]

    # Folder na pliki HTML
    output_folder = "downloaded_html"

    # Pobieranie plików HTML
    file_map = download_html_files(urls, output_folder)

    # Analiza danych i wyświetlanie wyników
    for url, file_path in file_map.items():
        data = fetch_trustpilot_data_from_html(file_path)
        print(f"Dane z linku {url}:")
        print(f"  Liczba opinii: {data['review_count']}")
        print(f"  Średnia ocena: {data['average_score']}")

    # Usuwanie plików HTML
    clean_up_files(file_map.values())


if __name__ == "__main__":
    main()
