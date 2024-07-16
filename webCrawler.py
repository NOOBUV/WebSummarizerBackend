from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


class WebCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()
        self.to_visit = set([base_url])
        self.domain = urlparse(base_url).netloc
        self.found_urls = set()

    def is_same_domain(self, url):
        return urlparse(url).netloc == self.domain

    def normalize_url(self, url):
        return url.rstrip('/')

    def crawl(self):
        while self.to_visit and len(self.found_urls) < 5:
            current_url = self.to_visit.pop()
            if current_url in self.visited:
                continue

            self.visited.add(current_url)

            try:
                response = requests.get(current_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(self.base_url, href)
                    normalized_url = self.normalize_url(full_url)

                    if self.is_same_domain(normalized_url) and normalized_url not in self.visited:
                        self.to_visit.add(normalized_url)
                        self.found_urls.add(normalized_url)

            except requests.RequestException as e:
                print(f"Failed to fetch {current_url}: {e}")

        return list(self.found_urls)[:5]
