import requests
from bs4 import BeautifulSoup

class CheatSheetScraper:
    def __init__(self, base_url="https://cheatsheetseries.owasp.org/cheatsheets/"):
        self.base_url = base_url

    def get_cheat_sheet_urls(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [
            self.base_url + link['href']
            for link in soup.find_all('a', href=True)
            if link['href'].endswith('.html')
        ]

    def extract_cheat_sheet_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', {'class': 'container'})
        return ' '.join(p.get_text() for p in content.find_all('p')) if content else ''

    def scrape_cheat_sheets(self):
        return {url: self.extract_cheat_sheet_content(url) for url in self.get_cheat_sheet_urls()}
