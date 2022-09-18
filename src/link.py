import requests
import re
import threading
import concurrent.futures
from sys import exit
from os import environ

TOKEN = environ["TOKEN"]

bad_links = []
warning_links = []
good_link_count = 0
thread_local = threading.local()

def write_summary(payload):
    with open("tmp.txt", "a") as file:
        file.write(f"{payload}\n")

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def scan_link(url):
    global good_link_count
    pattern = re.compile(
            "^https:\/\/github.com\/([1-9A-Za-z-_.]+)\/([1-9A-Za-z-_.#]+([^\/]|\b$))"
    )
    try:
        headers = ''
        file,line,link = url
        session = get_session()
        if "github.com" in link:
            matches = re.finditer(pattern, link)
            headers = {'Authorization': 'token ' + TOKEN}
            for match in matches:
                link=f"https://api.github.com/repos/{match.group(1)}/{match.group(2)}"
                print(f"{match.group()} --> converted to {link}")
        try:
            with session.get(link, headers=headers, timeout=15) as response:
                response = response.status_code
        except requests.exceptions.SSLError:
            print(f"---> SSL certificate error for link: {link}")
            bad_links.append((file, line, link))
        except requests.exceptions.ReadTimeout:
            print(f"---> Connection timed out for link: {link}")
            bad_links.append((file, line, link))
        except requests.exceptions.RequestException as err:
            if "Max retries exceeded with url" in str(err):
                print(f"Link connection failed, max retries reached: {link}")
                bad_links.append((file, line, link))
            else:
                print(f"---> Connection error: {err} for link: {link}")
                bad_links.append((file, line, link))
        except Exception as err:
            print(f"---> Unexpected exception occurred while making request: {err} for link: {link}")
        else:
            if response == 403:
                print(f"--> Link validity unkwown with 403 Forbidden return code for link: {link}")
                warning_links.append((file, line, link))
            elif response == 406:
                print(f"--> Link validity unkwown with 406 Not Acceptable return code for link: {link}")
                warning_links.append((file, line, link))
            elif response == 504:
                print(f"----> Error with status code 504 Gateway Timeout for link: {link}")
                bad_links.append((file, line, link))
            elif 561 >= response >= 400:
                print(f"----> Error with status code {response} for link: {link}")
                bad_links.append((file, line, link))
            elif response >= 300:  # between 300-400 HTTP REDIRECT
                print(f"--> Link redirecting with status code {response} for link: {link}")
                warning_links.append((file, line, link))
            elif response < 400:
                print(f"Link valid with status code {response}")
                good_link_count += 1
            elif response == 999:
                print("--> Linkedin specific return code 999")
                warning_links.append((file, line, link))
            else:
                print(f"--> Unknown return code {response} for link: {link}")
                warning_links.append((file, line, link))
    except Exception as e:
        print(e)


def all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(scan_link, sites)


def scan_links(links, verbose=False):
    all_sites(links)
    write_summary("# :link: Summary")
    write_summary(f":white_check_mark: Good links: {good_link_count}")
    write_summary(f":warning: Warning links: {len(warning_links)}")
    write_summary(f":no_entry_sign: Bad links: {len(bad_links)}")
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
