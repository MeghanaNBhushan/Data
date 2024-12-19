# Branch cleaner

This is a command line tool to clean up staled branches in Bibucket.

## Default behaviour

- Delete the branches with no activity (commits, PR updates) more than __90__ days. Can be adjusted with `--days` option
- Delete the __merged__ branches with no activity after __30__ days. Can be adjusted with `--days-merged` option

## Command line options

    usage: bitbucket_delete_old_branches.py [-h] --project PROJECT --repo REPO
                                            [--url URL] [--user USER]
                                            [--passw PASSW] [--days DAYS]
                                            [--days-merged DAYS_MERGED] [--force]
                                            [--dry-run] [--debug] [-l LOG_FILE]

    optional arguments:
    -h, --help            show this help message and exit
    --project PROJECT, -p PROJECT
                            BitBucket Project key (mandatory)
    --repo REPO, -r REPO  Repository to look into. (mandatory)
    --url URL, -b URL     Bitbucket url. (default: https://sourcecode01.de.bosch.com)
    --user USER, -u USER  Username to log in to Bitbucket as. If not specified,
                            .netrc data is used
    --passw PASSW, -pw PASSW
                            Password to log in to bitbucket with. If not
                            specified, .netrc data is used.
    --days DAYS, -d DAYS  Branches older than the specified number of days will
                            be considered old. (default: 90)
    --days-merged DAYS_MERGED, -dm DAYS_MERGED
                            Number of days to keep merged branches. (default: 30)
    --force, -f           Force delete branches without confirmation.
    --dry-run, -dr        Do not produce real deletion. Just logging.
    --debug               Debug logging mode enable
    -l LOG_FILE, --log_file LOG_FILE
                            Full path to log file

# Example

Check what branches can be deleted in PJPH/BSW_REPOSITORY with `debug` output.

    python3 ./bitbucket_delete_old_branches.py -u esi9lr -pw ******** -r BSW_REPOSITORY -p PJPH --debug --dry-run
