import wikipediaapi


class WikipediaFetcher:
    def __init__(self, language='en', user_agent=None):
        user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.wiki = wikipediaapi.Wikipedia(language=language, user_agent=user_agent)

    def get_company_info(self, company_name):
        page = self.wiki.page(company_name)

        if page.exists():
            company_info = {
                "Title": page.title,
                "Summary": page.summary,
                "Sections": self._get_sections(page.sections),
                "Related Links": list(page.links.keys()),
                "Categories": list(page.categories.keys()),
                "URL": page.fullurl
            }
            return company_info
        else:
            return f"The page for {company_name} does not exist on Wikipedia."

    def _get_sections(self, sections):
        section_info = []
        for section in sections:
            section_info.append({
                "Title": section.title,
                "Subsections": self._get_sections(section.sections)
            })
        return section_info

