#  Artifactory

-----------------------
```
usage: artifactoryw.py [-h] [-d] [-q] [--version] {clean} ...
```
The Artifactory script collection

```
optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Print debug information
  -q, --quiet  Print only errors
  --version    show program's version number and exit
```

## Cleanup in Artifactory. 
### Basic Usage

The Artifactory sub-commands:
```
  {clean}
    clean      Cleaning in Artifactory.
```
```    
usage: artifactoryw clean [-h] --url ARTIFACTORY_URL -r ARTIFACTORY_REPOSITORY
                          -t RETENTION_PERIOD -df {c,dl} [-u USERNAME]
                          [-p PASSWORD] [--dry-run]

optional arguments:
  -h, --help            show this help message and exit
  --url ARTIFACTORY_URL
                        The Artifactory URL.
  -r ARTIFACTORY_REPOSITORY, --repository ARTIFACTORY_REPOSITORY
                        The Artifactory repository.
  --include-path-pattern INCLUDE_PATH_PATTERN
                        Search only files whose path (excluding file name) matches pattern, using wildcard matching. 
                        A pattern can use '*' and '?' as wildcards. 
                        Example: '/path/to/dir*/where/file/is/?tored'.
  --exclude-list EXCLUDE_LIST
                        Comma-separated list of files to skip.
                        Pattern is {repo}/{path}/{name}.
                        Example: 'project-repository/path/to/item.zip,project-repository/path/to/item.jar'.
  -t RETENTION_PERIOD, --retention-period RETENTION_PERIOD
                        Time periods are specified with a number and one of
                        the following suffixes: - milliseconds "ms" - seconds
                        "s" - minutes "minutes" - days "d" - weeks "w" -
                        months "mo" - years "y" For example: -rp=5d
  -df {c,dl}, --domain-field {c,dl}
                        The Artifactory AQL domain field. - c , `created` When
                        the item was created. - dl, `downloaded` The last time
                        an item was downloaded.
  -u USERNAME, --username USERNAME
                        User for accessing Artifactory (default: current
                        user).
  -p PASSWORD, --password PASSWORD
                        Password for accessing Artifactory (prompt if not
                        provided).
  --dry-run             Set to True to disable communication with the
                        Artifactory.
```

### Example
The following example finds all items that were created up to two weeks ago (i.e. no later than two weeks ago) and deletes ones. Activate ```--dry-run``` if items should not be deleted. 
```
artifactoryw.py clean --url=http://localhost:8081/artifactory --username=admin --password=Password --repo=test-local-repo -t=2w -df=c
```
