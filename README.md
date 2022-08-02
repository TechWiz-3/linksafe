# Linksafe

Scan your repo for broken links. Whitelist links or files you wish to ignore.

## Example usage
```yaml
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run linksafe
        uses: TechWiz-3/linksafe@main
        with: # comma seperated lists
          # use relative paths, if no dirs specified root dir is scanned
          dirs: ".,./src,./src/subdir,./doc/website,./doc/more"
          # set to false by default
          verbose: true
          whitelist_links: "https://xyz.xyz"
          whitelist_files: "./doc/HACKING.md"
```

## More info

`https://example.com` and `http://localhost` are automatically ignored  

Each directory to be scanned must be specified directly, otherwise only the root dir will be scanned and subdirs will be ignored. At the same time, if you want the root dir AND subdirs to be scanned, remember to include a `.` as part of the list.  

Files and or links can be whitelisted i.e. ignored.  

Please note, with repos with a lot of links, a scan can take a LONG time, even up to 40+ minutes.

## Todo
- [ ] Recognition of remove yt videos
- [ ] Emoji HTTP code (optional)
