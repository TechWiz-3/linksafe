# Linksafe

Scan your repo for broken links. Whitelist links or files you wish to ignore.

## Example usage
```yaml
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run linksafe
        uses TechWiz-3/linksafe@main:
        with:
          dirs: "./src,./src/subdir,./doc/website,./doc/more"
          verbose: true
          whitelist_links: "https://xyz.xyz"
          whitelist_files: "./doc/HACKING.md"
```

## More info

`https://example.com` and `http://localhost` are automatically ignored  

Each directory to be scanned must be specified directly, otherwise only the root dir will be scanned and subdirs will be ignored.  

Files and or links can be whitelist i.e. ignore

## Todo
- [ ] Recognition of remove yt videos
- [ ] Emoji HTTP code
