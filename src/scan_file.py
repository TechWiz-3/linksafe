# main(match.group())
# main(match.group())
import re
from link import scan_links
from os import getenv
import os
from sys import argv

args = argv
if "--local-test" in args:
    directories = ["./"]
    verbose = True
    whitelist_links = ["https://img.shields.io/badge/style-black-black"]
else:

    try:
        verbose = getenv("INPUT_VERBOSE")
        whitelist_links = getenv("INPUT_WHITELIST_LINKS").split(",")
        whitelist_files = getenv("INPUT_WHITELIST_FILES").split(",")
        directories = getenv("INPUT_DIRS").split(",")
    except:
        print("Error loading env variables, please check your .github/workflows workflow")
        from sys import exit
        exit()


# pattern = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
pattern = re.compile(r"(http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])")
links = []
default_link_exclusion = []

# loop through the directories, e.g. [".", "./src", "./doc"]
for directory in directories:
    for file_object in os.scandir(directory):
        file = file_object.path
        if file_object.is_file() and not file.startswith("./."):
            if verbose:
                print(f"Scanning {file} file")
            # scan file
            for i, line in enumerate(open(file)):
                for match in re.finditer(pattern, line):
                    try:
                        if verbose:
                            print(match.group())
                    except Exception as e:
                        print(e)
                    else:
                        ignore = None
                        re_match = match.group()
                        for ignore_link in default_link_exclusion:
                            ignore = False
                            if ignore_link in re_match:
                               ignore = True
                               print(f"Link ignored (automatically): {re_match}")
                        for ignore_link in whitelist_links:
                            ignore = False
                            if ignore_link in re_match:
                                ignore = True
                                print(f"Link ignored (whitelist): {re_match}")
                        if ignore:
                            pass
                        else:
                            links.append((file, i+1, re_match))
                            if verbose == True:
                                print('Found on line %s: %s' % (i+1, match.group()))

print("\n\nLink check starting:\n")
try:
    scan_links(links, verbose=True)
except Exception as e:
    print(e)
