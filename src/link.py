import requests
from requests.adapters import HTTPAdapter
from sys import exit
import concurrent.futures
import threading

thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def scan_link(url):
    url = url[2]
    session = get_session()
    with session.get(url) as response:
        print(f"Read {response.status_code} from {url}")

def all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(scan_link, sites)

def scan_links(links, verbose=False):
    import time
    start_time = time.time()
    all_sites(links)
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"{duration} seconds")
