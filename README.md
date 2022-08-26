# Linksafe

Scan your repo for broken links. Whitelist links or files you wish to ignore. Works in private repos.  

Check out the [fast](https://github.com/TechWiz-3/linksafe/tree/fast) branch for lightning fast checking for large volumes very short run time.

## Example usage
```yaml
name: Link-check
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
          dirs: ".,./src,./src/data,./tests,./tests/pylint"
          # set to false by default
          verbose: true
          whitelist_links: "https://xyz.xyz"
          # use relative paths
          whitelist_files: "./doc/HACKING.md"
```

## More info

`https://example.com` and `http://localhost` are automatically ignored  

Each directory to be scanned must be specified directly, otherwise only the root dir will be scanned and subdirs will be ignored. At the same time, if you want the root dir AND subdirs to be scanned, remember to include a `.` as part of the list.  

Files and or links can be whitelisted i.e. ignored.  

Please note, with repos with a lot of links, a scan can take a LONG time, even up to 40+ minutes.

## Todo
- [ ] In depth error handling for user inputs (if they go wrong)
- [ ] Recognition of removed yt videos
- [ ] Emoji HTTP code (optional)
- [ ] Enforce HTTPS option
- [ ] Allow bad SSL cert option
- [ ] Possible repo replacements, aliases or moves if a gh repo link fails
- [ ] 429 error code

---
### 🎉 Commit labels
If you're interested in the commit labels used in this repo, check out my [git emoji](https://github.com/TechWiz-3/git-commit-emojis) project
