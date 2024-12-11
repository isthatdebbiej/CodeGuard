import requests
from bs4 import BeautifulSoup

class CheatSheetScraper:
    def __init__(self, base_url="https://cheatsheetseries.owasp.org/cheatsheets/"):
        self.base_url = base_url

    def get_cheat_sheet_urls(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        cheat_sheet_urls = [self.base_url + link['href'] for link in links if link['href'].endswith('.html')]
        return cheat_sheet_urls

    def extract_cheat_sheet_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', {'class': 'container'})
        paragraphs = content.find_all('p') if content else []
        text_content = ' '.join([p.get_text() for p in paragraphs])
        return text_content

    def scrape_cheat_sheets(self):
        cheat_sheet_urls = self.get_cheat_sheet_urls()
        cheat_sheets = {}
        for url in cheat_sheet_urls:
            content = self.extract_cheat_sheet_content(url)
            cheat_sheets[url] = content
        return cheat_sheets
