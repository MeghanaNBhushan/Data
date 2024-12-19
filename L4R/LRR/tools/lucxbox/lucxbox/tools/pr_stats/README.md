# pr_stats - Pull Request Statistics generation

-----------------------

## Usage 

```
usage: pr_stats.py [-h] [-m MAX_PRS] --project PROJECT --repo REPO --username
                   USERNAME --password PASSWORD [--loc] [-url BITBUCKET_URL]
                   [-d] [-q]

Pull Request Statistics generation

optional arguments:
  -h, --help            show this help message and exit
  -m MAX_PRS, --max-prs MAX_PRS
                        Maximum number of pull requests to fetch from
                        bitbucket (default: 9999).
  --project PROJECT
  --repo REPO
  --username USERNAME
  --password PASSWORD
  --loc                 Calculate the line of code by duration (might take a
                        long time).
  -url BITBUCKET_URL, --bitbucket_url BITBUCKET_URL
                        Bitbucket URL root ( default:
                        https://sourcecode.socialcoding.bosch.com ).
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
```