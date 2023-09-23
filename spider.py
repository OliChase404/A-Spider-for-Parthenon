import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
from datetime import datetime 
import threading
from rich import print
from rich.console import Console
from assets import *
import time
from concurrent.futures import ThreadPoolExecutor  # Import ThreadPoolExecutor

terminal_width = os.get_terminal_size().columns
console = Console()
def clear(): return os.system('tput reset')

class Spider:
    def __init__(self, start_url, max_depth, spider_assets):
        self.start_url = start_url
        self.max_depth = max_depth
        self.spider_assets = spider_assets
        self.visited_links = set()
        # Create a timestamp to be used in the folder name
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        # Extract the path component from the URL and use it in the folder name
        parsed_url = urlparse(start_url)
        # Combine the netloc and path components to create the folder name
        folder_name = f"{parsed_url.netloc}_{parsed_url.path.replace('/', '_')}"
        self.target_folder = f"{folder_name}_{timestamp}"
        os.makedirs(self.target_folder, exist_ok=True)
    
    def save_resource(self, url, content):
        parsed_url = urlparse(url)
        if parsed_url.path.endswith('/'):
            filename = os.path.join(self.target_folder, parsed_url.netloc, parsed_url.path, 'index.html')
        else:
            filename = os.path.join(self.target_folder, parsed_url.netloc, parsed_url.path.lstrip('/'))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(content)


    def crawl(self, url, depth, rate_limit=0, max_threads=10):
        if depth > self.max_depth:
            return

        if url in self.visited_links:
            return
        try:
            response = requests.get(url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
            
            # Add rate limiting: Sleep for a few seconds before each request
            time.sleep(rate_limit)
            
            if response.status_code == 200:
                self.visited_links.add(url)
                print(f"Downloading: {url} (Size: {len(response.content)} bytes)")
                self.save_resource(url, response.content)

                soup = BeautifulSoup(response.text, 'html.parser')

                # Create a ThreadPoolExecutor with a maximum number of threads
                with ThreadPoolExecutor(max_workers=max_threads) as executor:
                    # Spider links in <a href>
                    for link in soup.find_all('a', href=True):
                        next_url = urljoin(url, link['href'])
                        # Submit each URL to the executor for crawling
                        executor.submit(self.crawl, next_url, depth + 1)

                if self.spider_assets:
                    # Spider assets in CSS files
                    for link in soup.find_all('link', rel='stylesheet'):
                        css_url = urljoin(url, link['href'])
                        threading.Thread(target=self.crawl, args=(css_url, depth + 1)).start()
                    
                    # Spider assets in JavaScript files
                    for script in soup.find_all('script', src=True):
                        js_url = urljoin(url, script['src'])
                        threading.Thread(target=self.crawl, args=(js_url, depth + 1)).start()

        except Exception as e:
            print(f"Error downloading {url}: {e}")

    def shutdown(self):
        self.executor.shutdown()



#----------------------------------------- Interface -----------------------------------------
def main_menu():
    banner()
    choice = input('Enter Target URL-->>> ')
    if choice == '':
        clear()
        main_menu()
    else:
        start_url = choice
    print('URL: ' + start_url)
    choice = input('Enter Max Recursion Depth-->>> ')
    if choice == '':
        print('Please enter a number')
        main_menu()
    else:
        max_depth = int(choice)
    print('Max Depth: ' + str(max_depth))
    choice = input('Spider Assets? (y/n)-->>> ')
    if choice == 'y':
        spider_assets = True
    else:
        spider_assets = False
    print('Spider Assets: ' + str(spider_assets))

    choice = input('Use rate limiting? (y/n)-->>> ')
    if choice == 'y':
        max_requests = input('Enter max requests per second--->>>')
        rate_limit = 1 / int(max_requests)
        print('Rate Limit: ' + str(max_requests) + ' requests per second')
    else: 
        rate_limit = 0
        print('Rate Limit: None')

    max_threads = input('Enter max threads-->>> ')
    if max_threads == '':
        max_threads = 10
    else:
        max_threads = int(max_threads)
    print('Max Threads: ' + str(max_threads))

    choice = input('Start Spider? (y/n)-->>> ')
    if choice == 'y':
        crawler = Spider(start_url, max_depth, spider_assets)
        crawler.crawl(start_url, 0, rate_limit, max_threads)
        crawler.shutdown()
    elif choice == 'n':
        clear()
        main_menu()

#-----------------------------------------

if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Philosophy"
    max_depth = 2
    spider_assets = True

    clear()
    main_menu()
