import requests
from requests.adapters import HTTPAdapter


def scan_links(links, verbose=False):
    bad_links = False
    for link in links:
        print(link)
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
                print("Error with status code ", req.status_code)
                bad_links = True
            elif status < 400:
                print(f"Link valid with status code {req.status_code}")
    if not bad_links:
        print("All links correct - test passed")
    else:
        print("Test failed")
