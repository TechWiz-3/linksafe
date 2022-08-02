import requests
from requests.adapters import HTTPAdapter
from sys import exit

def scan_links(links, verbose=False):
    bad_links = []
    warning_links = []
    for file, line, link in links:
        try:
            s = requests.Session()
            s.mount(link, HTTPAdapter(max_retries=5))
            req = s.get(link)
            status = req.status_code
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
            if status == 403:
                print(f"--> Link validity unkwown with 403 Forbidden return code")
                warning_links.append((file, line, link))
            elif status == 406:
                print(f"--> Link validity unkwown with 406 Not Acceptable return code")
                warning_links.append((file, line, link))
            elif 561 >= status >= 400:
                print(f"----> Error with status code {status}")
                bad_links.append((file, line, link))
            elif status >= 300:  # between 300-400 HTTP REDIRECT
                print(f"--> Link redirecting with status code {status}")
                warning_links.append((file, line, link))
            elif status < 400:
                print(f"Link valid with status code {status}")
            elif status == 999:
                print("--> Linkedin specific return code 999")
                warning_links.append((file, line, link))
            else:
                print(f"--> Unknown return code {status}")
                warning_links.append((file, line, link))
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
