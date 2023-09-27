import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
from datetime import datetime 
from rich import print
from rich.console import Console
from assets import *
import time
from concurrent.futures import ThreadPoolExecutor
import hashlib


terminal_width = os.get_terminal_size().columns
console = Console()
def clear(): return os.system('tput reset')


class Spider:
    def __init__(self, start_url, max_depth, spider_assets, spider_images):
        self.start_url = start_url
        self.max_depth = max_depth
        self.spider_assets = spider_assets
        self.spider_images = spider_images
        self.visited_links = set()
        # Create a timestamp to be used in the folder name
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        # Extract the path component from the URL and use it in the folder name
        parsed_url = urlparse(start_url)
        # Combine the netloc and path components to create the folder name
        folder_name = f"{parsed_url.netloc}_{parsed_url.path.replace('/', '_')}"
        self.target_folder = f"{folder_name}_{timestamp}"
        os.makedirs(self.target_folder, exist_ok=True)

    def crawl(self, url, depth, rate_limit=0, max_threads=4):
        if depth > self.max_depth:
            return

        if url in self.visited_links:
            return

        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})

            # Add rate limiting
            time.sleep(rate_limit)

            if response.status_code == 200:
                self.visited_links.add(url)
                print(f"Downloading: {url} (Size: {len(response.content)} bytes)")
                self.save_resource(url, response.content)

                soup = BeautifulSoup(response.text, 'html.parser')

                # Collect CSS and JavaScript assets
                css_assets = [urljoin(url, link['href']) for link in soup.find_all('link', rel='stylesheet')]
                js_assets = [urljoin(url, script['src']) for script in soup.find_all('script', src=True)]
                images = [urljoin(url, img['src']) for img in soup.find_all('img', src=True)]

                # Create a ThreadPoolExecutor with a maximum number of threads to crawl assets
                with ThreadPoolExecutor(max_workers=max_threads) as executor:
                    # Spider links in <a href>
                    for link in soup.find_all('a', href=True):
                        next_url = urljoin(url, link['href'])
                        # Submit each URL to the executor for crawling
                        executor.submit(self.crawl, next_url, depth + 1)

                    if self.spider_assets:
                        # Crawl CSS and JavaScript assets in parallel threads
                        executor.submit(self.crawl, css_assets, depth + 1, max_threads)
                        executor.submit(self.crawl, js_assets, depth + 1, max_threads)

                    if self.spider_images:
                        # Crawl images in parallel threads
                        executor.submit(self.crawl_images, images, depth + 1, max_threads)

        except Exception as e:
            print(f"Error downloading {url}: {e}")
    
    def save_resource(self, url, content):
        parsed_url = urlparse(url)
        if parsed_url.path.endswith('/'):
            filename = os.path.join(self.target_folder, parsed_url.netloc, parsed_url.path, 'index.html')
        else:
            filename = os.path.join(self.target_folder, parsed_url.netloc, parsed_url.path.lstrip('/'))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(content)


    def crawl_images(self, image_urls, depth, max_threads=4):
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                for img_url in image_urls:
                    
                    # Skip Data URLs
                    if img_url.startswith('data:image/'):
                        print(f"Skipping Data URL: {img_url}")
                        continue
                    
                    try:
                        response = requests.get(img_url, headers={"User-Agent": "Your User Agent Here"})

                        if response.status_code == 200:
                            print(f"Downloading Image: {img_url} (Size: {len(response.content)} bytes)")
                            self.save_image(img_url, response)
                        else:
                            print(f"Failed to download Image: {img_url} (Status Code: {response.status_code})")

                    except Exception as e:
                        print(f"Error downloading {img_url}: {e}")

    def save_image(self, url, response):
        parsed_url = urlparse(url)
        
        # Try to get the file extension from the URL
        image_extension = os.path.splitext(parsed_url.path)[1]
        
        if not image_extension:
            # If the extension couldn't be extracted from the URL, try to get it from the Content-Type header
            content_type = response.headers.get('Content-Type', '')
            if content_type.startswith('image/'):
                image_extension = '.' + content_type.split('/')[-1]
            else:
                # If no valid extension can be determined, default to .jpg (you can change this as needed)
                image_extension = '.jpg'

        # Generate a unique filename
        image_hash = hashlib.md5(url.encode()).hexdigest()
        filename = os.path.join(self.target_folder, 'images', f"{image_hash}{image_extension}")
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            f.write(response.content)

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

    choice = input('Spider Images? (y/n)-->>> ')
    if choice == 'y':
        spider_images = True
    else:
        spider_images = False
    print('Spider Images: ' + str(spider_images))

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
        crawler = Spider(start_url, max_depth, spider_assets, spider_images)
        crawler.crawl(start_url, 0, rate_limit, max_threads)
    elif choice == 'n':
        clear()
        main_menu()

#-----------------------------------------


#-----------Initialise Spider-------------
if __name__ == "__main__":
    clear()
    main_menu()
#-----------------------------------------