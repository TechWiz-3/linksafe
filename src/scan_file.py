#!/usr/bin/env python3
import re
from link import scan_links
import os
from sys import argv
from sys import exit

args = argv
if "--local-test" in args:  # for local testing
   # directories = ["./", "./pythonfetch", "./bfetch/", "./kids.cache/", "awesome-python"]
    directories = '.'
#    directories = ["awesome-python"]
    verbose = True
    whitelist_links = ["https://img.shields.io/badge/style-black-black", "http://github.com/0k/%%name%%"]
    whitelist_files=["LICENSE.md", "README.md"]
    for i, file in enumerate(whitelist_files):
        if not file.startswith("./"):
            whitelist_files[i] = f"./{file}"
            print(f"File '{file}' has been converted to relative filepath '{whitelist_files[i]}'")

else:
    try:
        verbose = os.getenv("INPUT_VERBOSE")
        whitelist_links = os.getenv("INPUT_WHITELIST_LINKS").split(",")
        whitelist_files = os.getenv("INPUT_WHITELIST_FILES").split(",")
        directories = os.getenv("INPUT_DIRS").split(",")  # defaults to '.' from the action.yml
        if verbose == "false":
            verbose = False
            print("Verbose is disabled")
        elif verbose == "true":
            verbose = True
            print("Verbose is enabled")
        for i, file in enumerate(whitelist_files):
            if not file.startswith("./"):
                whitelist_files[i] = f"./{file}"
                print(f"File '{file}' has been converted to relative filepath '{whitelist_files[i]}'")
    except:
        print("Error loading env variables, please check your .github/workflows workflow")
        exit(1)


pattern = re.compile(r"(http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])")
links = []
default_link_exclusion = ["https://example.com", "http://example.com", "http://localhost", "http://localhost"]

# loop through the directories, e.g. [".", "./src", "./doc"]
for directory in directories:
    if directory != "." and not directory.startswith("./"):
        old_directory = directory
        directory = f"./{directory}"
        print(f"Directory '{old_directory}' converted to relative filepath '{directory}'")
    try:
        scan = os.scandir(directory)
    except FileNotFoundError:
        print(f"Directory '{directory}' not found, please check the file path (only use relative paths) and spelling")
        exit(78)
    for file_object in scan:
        file = file_object.path
        if file_object.is_file() and not file.startswith("./."):  # filter out dirs like .git
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
                            pass
    #                        print(f"Link found on line {i+1}: {re_match}")
                    except Exception as e:
                        print(e)
                    else:
                        ignore = False
                        for ignore_link in default_link_exclusion:
                            if ignore_link in re_match:
                               print(f"Link ignored (automatically): {re_match}")
                               ignore = True
                               break
                        if ignore:  # link should be automatically ignored
                            continue  # skip to the next link
                        for ignore_link in whitelist_links:
                            if ignore_link in re_match:
                                print(f"Link ignored (whitelist): {re_match}")
                                break
                        else:  # if link is not whitelisted or ignored
                            links.append((file, i+1, re_match))
                            if verbose == True:
  #                              print('Link added for scanning %s' % (match.group()))
                                pass

print("\n\nLink check starting:\n")
try:
    scan_links(links, verbose=True)
except Exception as e:
    print(e)
