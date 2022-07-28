#!/usr/bin/env python3
import re
from link import scan_links
from os import getenv
import os
from sys import argv

args = argv
if "--local-test" in args:
   # directories = ["./", "./pythonfetch", "./bfetch/", "./kids.cache/", "awesome-python"]
    directories = ["./awesome-python"]
    verbose = True
    whitelist_links = ["https://img.shields.io/badge/style-black-black", "http://github.com/0k/%%name%%"]
    whitelist_files=["./LICENSE.md"]
else:
    try:
        verbose = getenv("INPUT_VERBOSE")
        whitelist_links = getenv("INPUT_WHITELIST_LINKS").split(",")
        whitelist_files = getenv("INPUT_WHITELIST_FILES").split(",")
        directories = getenv("INPUT_DIRS").split(",")
        if verbose = "false":
            verbose == False
            print("Verbose is disabled")
        elif verbose == "true":
            verbose = True
            print("Verbose is enabled")
    except:
        print("Error loading env variables, please check your .github/workflows workflow")
        from sys import exit
        exit(1)


pattern = re.compile(r"(http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])")
links = []
default_link_exclusion = ["https://example.com", "http://localhost"]

# loop through the directories, e.g. [".", "./src", "./doc"]
for directory in directories:
    for file_object in os.scandir(directory):
        file = file_object.path
        if file_object.is_file() and not file.startswith("./."):
            if file in whitelist_files:
                print(f"{file} skipped due to whitelist")
                # skip the file
                continue
            if verbose:
                print(f"Scanning {file} file")
            # scan file
            for i, line in enumerate(open(file)):
                for match in re.finditer(pattern, line):
                    try:
                        re_match = match.group()
                        if verbose:
                            print(f"Link found on line {i+1}: {re_match}")
                    except Exception as e:
                        print(e)
                    else:
                        ignore = None
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
                                print('Link added for scanning %s' % (match.group()))

print("\n\nLink check starting:\n")
try:
    scan_links(links, verbose=True)
except Exception as e:
    print(e)
