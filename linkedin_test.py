from linkedin_api.linkedin import Linkedin
from linkedin_api.cookie_repository import LinkedinSessionExpired
import os


class LinkedinFetcher:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api = self.authenticate()

    def clear_session_cookies(self):
        try:
            cookie_dir = os.path.expanduser("~/.linkedin_api_cookies")
            if os.path.exists(cookie_dir):
                print("Clearing cached cookies...")
                for file in os.listdir(cookie_dir):
                    file_path = os.path.join(cookie_dir, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Error deleting cookie file: {e}")
            else:
                print("No cookie directory found, skipping cookie clear.")
        except Exception as e:
            print(f"Error clearing cookie directory: {e}")

        print("Attempting to clear cookies from repository directly.")
        try:
            client = Linkedin(self.username, self.password)
            client.client._cookie_repository.clear()
            print("Cleared cookies from the cookie repository.")
        except Exception as e:
            print(f"Error clearing cookies from repository: {e}")

    def authenticate(self):
        try:
            return Linkedin(self.username, self.password)
        except LinkedinSessionExpired:
            print("LinkedIn session expired. Attempting to re-authenticate...")
            self.clear_session_cookies()  # Clear cookies
            return Linkedin(self.username, self.password)

    def get_linkedin_data(self, company_name):
        try:
            company_data = self.api.get_company(company_name)
            return company_data
        except Exception as e:
            return f"An error occurred: {str(e)}"


class LinkedinTester:
    def __init__(self, username, password):
        self.linkedin_fetcher = LinkedinFetcher(username, password)

    def test_company_fetch(self, company_name):
        print(f"Testing LinkedIn data fetch for company: {company_name}")
        company_data = self.linkedin_fetcher.get_linkedin_data(company_name)
        if isinstance(company_data, dict):
            print("LinkedIn data fetched successfully:")
            self.pretty_print(company_data)
        else:
            print(f"Failed to fetch LinkedIn data: {company_data}")

    def pretty_print(self, data, indent=0):
        spacing = '    ' * indent
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    print(f"{spacing}{key}:")
                    self.pretty_print(value, indent + 1)
                elif isinstance(value, list):
                    print(f"{spacing}{key}:")
                    for item in value:
                        self.pretty_print(item, indent + 1)
                else:
                    print(f"{spacing}{key}: {value}")
        else:
            print(f"{spacing}{data}")


if __name__ == "__main__":
    username = "artur.oleksiewicz.work@gmail.com"
    password = "Sto1noga$"

    company_name = "Microsoft"

    tester = LinkedinTester(username, password)
    tester.test_company_fetch(company_name)
