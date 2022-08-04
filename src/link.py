import requests
from requests.adapters import HTTPAdapter
from sys import exit
import concurrent.futures
import threading

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = resuests.Session()
    return thread_local.session

def scan_link(url, session):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {response.status_code} from {url}")
    except Exception as err:
        print(err)

def all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5):
        executor.map(download_site, sites)

def scan_links(links, verbose=False):
    all_sites(links)
