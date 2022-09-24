# Linksafe

## 🕴️⚡Clean Fast Branch

Scan your repo for broken links. Whitelist links or files you wish to ignore. Works in private repos.  

This branch is like [fast](https://github.com/TechWiz-3/linksafe/tree/fast), except it's logs are cleaner as it runs without creating an action summary.


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
        uses: TechWiz-3/linksafe@fast
        with: # comma seperated lists
          # use relative paths, if no dirs specified root dir is scanned
          dirs: ".,./src,./src/data,./tests,./tests/pylint"
          # set to false by default
          verbose: true
          whitelist_links: "https://xyz.xyz"
          # use relative paths
          whitelist_files: "./doc/HACKING.md"
        env:
            TOKEN: ${{ secrets.TOKEN }}
```

## Setup

#### :key: Generate a github token (no extra perms required)
How-to [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

#### :lock: Create a repo secret called `TOKEN`
How-to [here](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)

#### :thumbsup: Enjoy lightning speed link checking

### How

To avoid github ratelimits from the huge volume of lightning fast requests, use of a github token is required if github repo links are used. The program uses regex to recognise github repo links and converts them to a github api endpoint `https://api.github.com/repos/user/repo`

## More info

`https://example.com` and `http://localhost` are automatically ignored  

Each directory to be scanned must be specified directly, otherwise only the root dir will be scanned and subdirs will be ignored. At the same time, if you want the root dir AND subdirs to be scanned, remember to include a `.` as part of the list.  

Files and or links can be whitelisted i.e. ignored.  

## Todo
- [ ] In depth error handling for user inputs (if they go wrong)
- [ ] Recognition of remove yt videos
- [ ] Emoji HTTP code (optional)

---
### 🎉 Commit labels
If you're interested in the commit labels used in this repo, check out my [git emoji](https://github.com/TechWiz-3/git-commit-emojis) project
