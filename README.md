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
    linksafe:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run linksafe
      uses TechWiz-3/linksafe@main
      with:
        dirs: "./src,./src/subdir,./doc/website,./doc/more"
        verbose: true
        whitelist_links: "https://xyz.xyz"
        whitelist_files: "./doc/HACKING.md"
```

## Todo
- [ ] Recognition of remove yt videos
