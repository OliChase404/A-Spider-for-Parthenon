import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
from datetime import datetime
import threading
import time
from rich import print
from rich.console import Console
from assets import *
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor

# ... (your existing code)

class Spider:
    # ... (your existing code)

    def crawl(self, url, depth):
        if depth > self.max_depth:
            return

        if url in self.visited_links:
            return

        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
            
            # Add rate limiting: Sleep for a few seconds before each request
            time.sleep(2)  # Adjust the delay as needed (2 seconds in this example)

            if response.status_code == 200:
                self.visited_links.add(url)
                print(f"Downloading: {url} (Size: {len(response.content)} bytes)")
                self.save_resource(url, response.content)

                soup = BeautifulSoup(response.text, 'html.parser')

                # Create a ThreadPoolExecutor with a maximum number of threads
                with ThreadPoolExecutor(max_workers=10) as executor:
                    # Spider links in <a href>
                    for link in soup.find_all('a', href=True):
                        next_url = urljoin(url, link['href'])
                        # Submit each URL to the executor for crawling
                        executor.submit(self.crawl, next_url, depth + 1)

                    if self.spider_assets:
                        # Spider assets in CSS files
                        for link in soup.find_all('link', rel='stylesheet'):
                            css_url = urljoin(url, link['href'])
                            executor.submit(self.crawl, css_url, depth + 1)

                        # Spider assets in JavaScript files
                        for script in soup.find_all('script', src=True):
                            js_url = urljoin(url, script['src'])
                            executor.submit(self.crawl, js_url, depth + 1)

        except Exception as e:
            print(f"Error downloading {url}: {e}")

# ... (your existing code)

if __name__ == "__main__":
    # ... (your existing code)
