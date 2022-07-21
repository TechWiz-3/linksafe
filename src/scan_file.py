import re
from link import scan_links
from os import getenv
import os
from sys import argv

#args = argv
#if "--local" in args:
#    verbose = args[2]
#    # etc etc
#else:
#
#    try:
#        verbose = getenv("INPUT_VERBOSE")
#        whitelist_links = getenv("INPUT_WHITELIST_LINKS").split(",")
#        whitelist_files = getenv("INPUT_WHITELIST_FILES").split(",")
#        directories = getenv("INPUT_DIRS").split(",")
#    except:
#        print("Error loading env variables, please check your .github/workflows workflow")
#        from sys import exit
#        exit()

# set env variables locally to be able to test locally

directories = ["./"]
verbose = True

pattern = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")
links = []

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
                        print(match.group())
                    except Exception as e:
                        print(e)
                    else:
                        links.append(match.group())
                        if verbose == True:
                            print('Found on line %s: %s' % (i+1, match.group()))

print("Link check start:\n")
print(links)
try:
    scan_links(links, verbose=True)
except Exception as e:
    print(e)
# main(match.group())
