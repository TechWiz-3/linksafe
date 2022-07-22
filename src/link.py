import requests
from requests.adapters import HTTPAdapter


def scan_links(links, verbose=False):
    bad_links = []
    for file, line, link in links:
        try:
            s = requests.Session()
            s.mount(link, HTTPAdapter(max_retries=5))
            req = s.get(link)
            status = req.status_code
        except Exception as err:
            #raise SystemExit(err)
            print(err)
            #pass
        else:
            if status >= 400:
                print("Error with status code", req.status_code)
                bad_links.append((file, line, link))
            elif status < 400:
                print(f"Link valid with status code {req.status_code}")
    if bad_links:
        print("Test failed")
        for file, line, link in bad_links:
            print(f"In {file} on line {line}, link: {link}")
    else:
        print("All links correct - test passed")
