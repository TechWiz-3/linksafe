import requests
from requests.adapters import HTTPAdapter
from sys import exit
import concurrent.futures
import threading

bad_links = []
warning_links = []
thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def scan_link(url):
    file,line,link = url
    session = get_session()
    try:
        with session.get(url) as response:
            print(f"Read {response.status_code} from {url}")
    except requests.exceptions.SSLError:
        print(f"---> SSL certificate error for link: {link}")
        bad_links.append((file, line, link))
    except requests.exceptions.RequestException as err:
        if "Max retries exceeded with url" in str(err):
            print(f"Link connection failed, max retries reached: {link}")
            bad_links.append((file, line, link))
        else:
            print(f"---> Connection error: {err}")
            bad_links.append((file, line, link))
    except Exception as err:
        print(f"---> Unexpected exception occurred while making request: {err}")
    else:
        if response == 403:
            print(f"--> Link validity unkwown with 403 Forbidden return code")
            warning_links.append((file, line, link))
        elif response == 406:
            print(f"--> Link validity unkwown with 406 Not Acceptable return code")
            warning_links.append((file, line, link))
        elif 561 >= response >= 400:
            print(f"----> Error with status code {response}")
            bad_links.append((file, line, link))
        elif response >= 300:  # between 300-400 HTTP REDIRECT
            print(f"--> Link redirecting with status code {response}")
            warning_links.append((file, line, link))
        elif response < 400:
            print(f"Link valid with status code {response}")
        elif response == 999:
            print("--> Linkedin specific return code 999")
            warning_links.append((file, line, link))
        else:
            print(f"--> Unknown return code {response}")
            warning_links.append((file, line, link))

def all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(scan_link, sites)

def scan_links(links, verbose=False):
    all_sites(links)
    if bad_links:
        print("Test failed")
        if warning_links:
            print("\n==== Links with non-definitive status codes ====")
            for file, line, link in warning_links:
                print(f"In {file} on line {line}, link: {link}")
            print("Links that you have verified are OK can be whitelisted in the workflow file")
        print("\n==== Failed links ====")
        for file, line, link in bad_links:
            print(f"In {file} on line {line}, link: {link}")
        exit(1)
    elif warning_links:
        print("\n==== Links with non-definitive status codes ====")
        for file, line, link in warning_links:
            print(f"In {file} on line {line}, link: {link}")
        print("Links that you have verified are OK can be whitelisted in the workflow file")
        print("Otherwise, all links correct - test passed")
    else:
        print("All links correct - test passed")
