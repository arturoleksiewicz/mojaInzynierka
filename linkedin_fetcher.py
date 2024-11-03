import os
from linkedin_api import Linkedin
from linkedin_api.cookie_repository import LinkedinSessionExpired

class LinkedinFetcher:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api = self.authenticate()

    def authenticate(self):
        try:
            return Linkedin(self.username, self.password)
        except LinkedinSessionExpired:
            # Re-authenticate if the session is expired
            cookie_file = f'cookies_{self.username}.json'
            if os.path.exists(cookie_file):
                os.remove(cookie_file)
            return Linkedin(self.username, self.password)

    def get_linkedin_data(self, company_name):
        try:
            company_data = self.api.get_company(company_name)
            return company_data
        except LinkedinSessionExpired:
            # Re-authenticate and try again
            self.api = self.authenticate()
            try:
                company_data = self.api.get_company(company_name)
                return company_data
            except Exception as e:
                return f"An error occurred after re-authentication: {e}"
        except Exception as e:
            return f"An error occurred: {e}"
