#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
import pandas as pd
from tabulate import tabulate
import smtplib


from datetime import timedelta
from time import time
from time import sleep
from modules.bitbucket import BitBucket
from modules.functions import compile_regex_from_list, yes_no


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Global variables
WHITELISTED_BRANCHES_CONFIGS_DIR = "config"

BRANCH_INFO_AHEAD_BEHIND = "com.atlassian.bitbucket.server.bitbucket" \
                           "-branch:ahead-behind-metadata-provider"
BRANCH_INFO_LATEST_COMMIT = "com.atlassian.bitbucket.server.bitbucket" \
                            "-branch:latest-commit-metadata"
BRANCH_INFO_OUTGOING_PR = "com.atlassian.bitbucket.server.bitbucket" \
                          "-ref-metadata:outgoing-pull-request-metadata"

SERVER = "rb-smtp-int.bosch.com"
FROM = "system-user-CC.C_Integration_ATR@bcn.bosch.com"


class BranchDeleter:

    def __init__(self, url, project, repository, user, password,
                 older_than_days, days_after_merge, force, dry_run):
        """
        Class to handle operations for deletions of obsolete branches and all
        internal methods.

        Main method: `run`
        :param url: Required String: Bitbucket url
        :param project: Required String: BitBucket project key
        :param repository: Required String: BitBucket repository
        :param user: Required String: Bitbucket user
        :param password: Required String: Bitbucket password
        :param older_than_days: Required int: Days to consider branch old
        :param days_after_merge: Required int: Days to keep merged branches
        :param force: Required boolean: If ask an approval for deletion
        :param dry_run: Required boolean: Do not provide any real actions, just
        logging if true
        """
        self.bitbucket = BitBucket(url, project, repository, user, password)
        self.older_than_days = older_than_days
        self.days_after_merge = days_after_merge
        self.force = force
        self.dry_run = dry_run

        self.total_branches_before = 0
        self.old_branches = []
        self.whitelisted_branches = []
        self.locked_branches = []
        self.deleted_branches = 0
        self.mail_info = pd.DataFrame()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_rel_path = os.path.join(WHITELISTED_BRANCHES_CONFIGS_DIR,
                                       project, "{}.json".format(repository))

        self.whitelist_file_path = os.path.join(script_dir, config_rel_path)

    def delete(self):
        """
        Deletes old branches older than `older_than_days` and merged branches
        older than `days_after_merge` and don't have active pull-requests last
        `older_than_days` from repository.
        :return: None
        """
        logger.info("Searching for whitelis patterns in {}".format(
            self.whitelist_file_path))

        with open(self.whitelist_file_path) as f:
            whitelisted_branches = json.loads(f.read())["whitelist"]

        whitelist_check_regex = compile_regex_from_list(whitelisted_branches)
        logger.info("Whitelist patterns: {}".format(whitelisted_branches))

        for branch in self.bitbucket.get_all_branches(details=True):

            self.total_branches_before += 1

            if whitelist_check_regex.search(branch["displayId"]):
                logger.debug("Branch {} is in the whitelist, skipping".format(
                    branch["displayId"]))
                self.whitelisted_branches.append(branch)
                continue

            commit_age_days = self.get_branch_head_age_days(branch)

            if (commit_age_days > self.days_after_merge and
                    self.branch_is_not_ahead(branch)):
                logger.debug("Branch {} is {} days old and was merged. "
                             "Will be deleted".format(branch["displayId"],
                                                      commit_age_days))
                self.old_branches.append(branch)
                continue

            if commit_age_days > self.older_than_days:
                if self.branch_pr_activity_not_older_than_days(
                        branch, self.older_than_days):
                    logger.debug(
                        "Branch {} is {} days old, but has opened PRs"
                        " for last {} days. Will not be deleted".format(
                            branch["displayId"], commit_age_days,
                            self.older_than_days))
                    continue

                logger.debug("Adding {} branch to deletion list".format(
                    branch["displayId"]))
                self.old_branches.append(branch)

            else:
                logger.debug(
                    "Branch {} is {} days old (<{} days). "
                    "Will not be deleted".format(branch["displayId"],
                                                 commit_age_days,
                                                 self.older_than_days))

        if len(self.old_branches) > 0:
            if not self.force:
                question = "Found {} branches older than {} days:".format(
                    len(self.old_branches), self.older_than_days)
                for old_branch in self.old_branches:
                    question += "\n{}".format(old_branch["displayId"])
                question += "\nShould these branches be deleted?"
                if yes_no(question):
                    self.delete_old_branches()
            else:
                logger.info("Found {} old branches:".format(
                    len(self.old_branches)))
                self.delete_old_branches()
        else:
            logger.warning("No branches for deletion found!".format())

        logger.info("Branches filtered by whitelist:\n{}".format(
            '\n'.join([b["displayId"] for b in self.whitelisted_branches])))
        left_branches = sum(1 for x in self.bitbucket.get_all_branches())
        self.deleted_branches = \
            len(self.old_branches) - len(self.locked_branches)
        logger.info("""
            ================================
                Branches before deletion:{}.
                Deleted branches:{}.
                Whitelisted branches:{}.
                Locked branches: {}.
                Branches left: {}.
            """.format(self.total_branches_before,
                       self.deleted_branches,
                       len(self.whitelisted_branches),
                       len(self.locked_branches),
                       left_branches))
        
        logger.info(branch)

    def mail(self):
        """
        Deletes old branches older than `older_than_days` and merged branches
        older than `days_after_merge` and don't have active pull-requests last
        `older_than_days` from repository.
        :return: None
        """
        logger.info("Searching for whitelis patterns in {}".format(
            self.whitelist_file_path))

        with open(self.whitelist_file_path) as f:
            whitelisted_branches = json.loads(f.read())["whitelist"]

        whitelist_check_regex = compile_regex_from_list(whitelisted_branches)
        logger.info("Whitelist patterns: {}".format(whitelisted_branches))

        for branch in self.bitbucket.get_all_branches(details=True):

            self.total_branches_before += 1

            if whitelist_check_regex.search(branch["displayId"]):
                logger.debug("Branch {} is in the whitelist, skipping".format(
                    branch["displayId"]))
                self.whitelisted_branches.append(branch)
                continue

            commit_age_days = self.get_branch_head_age_days(branch)

            if (commit_age_days > self.days_after_merge and
                    self.branch_is_not_ahead(branch)):
                logger.debug("Branch {} is {} days old and was merged. "
                             "Should be deleted".format(branch["displayId"],
                                                      commit_age_days))
                self.old_branches.append(branch)
                continue

            if commit_age_days > self.older_than_days:
                if self.branch_pr_activity_not_older_than_days(
                        branch, self.older_than_days):
                    logger.debug(
                        "Branch {} is {} days old, but has opened PRs"
                        " for last {} days".format(
                            branch["displayId"], commit_age_days,
                            self.older_than_days))
                    continue

                logger.debug("Adding {} branch to deletion list".format(
                    branch["displayId"]))
                self.old_branches.append(branch)

            else:
                logger.debug(
                    "Branch {} is {} days old (<{} days). "
                    "Will not be deleted".format(branch["displayId"],
                                                 commit_age_days,
                                                 self.older_than_days))

        if len(self.old_branches) > 0:
            for old_branch in self.old_branches:
                committer = self.branch_last_committer_name(old_branch)
                committer_email = self.branch_last_committer_email(old_branch)
                commit_age_days = self.get_branch_head_age_days(old_branch)
                self.mail_info.index.name = 'branch name'
                self.mail_info.loc[old_branch["displayId"],'lastCommit'] = old_branch['latestCommit']
                self.mail_info.loc[old_branch["displayId"],'daysAgo'] = commit_age_days
                self.mail_info.loc[old_branch["displayId"],'email'] = committer_email
                self.mail_info.loc[old_branch["displayId"],'committer'] = committer


            for mail_id in self.mail_info.email.unique() :

                logger.info(mail_id)

                TO = [mail_id] # must be a list

                SUBJECT = 'Old Branches in the ARAS repository'
                mail_body = (self.mail_info[self.mail_info['email'] == mail_id]).drop(['committer', 'email'], axis = 1)
                mail = """Subject: {}\n\nHello,

You seem to have some branches that have not been touched in a long time.

Please delete the branches from the remote if they are not needed.

You can keep your local branch if you wish (you will then stop receiving this reminder).


To delete a remote branch use:

git push -d <remote name> <branch to delete>

normally <remote name> is origin.

 

Your old branches are:\n{}

 

This email is auto-generated.

 

Have a nice day.

Best Regards, 
Annoying Mail Generator
                """.format(SUBJECT, tabulate( mail_body, headers='keys', tablefmt='psql') )
                

                    
                    
                    # Send the mail
                server = smtplib.SMTP(SERVER)
                server.login("de\cis9lr", "CoIntATR2024")
                server.sendmail(FROM, TO, mail)
                server.quit()        
                sleep(3)
        else:
                logger.warning("No branches for deletion found!".format())

        logger.info("""
            ================================        
                Branches filtered by whitelist:\n{}""".format(
            '\n'.join([b["displayId"] for b in self.whitelisted_branches])))

        self.deleted_branches = \
            len(self.old_branches) - len(self.locked_branches)

        logger.info("""
            ================================
                Branches to be deleted:{}.
                Whitelisted branches:{}.
                Locked branches: {}.
            """.format(self.total_branches_before,
                       len(self.whitelisted_branches),
                       len(self.locked_branches)))
        

    def branch_last_committer_name(self, branch):
        """
        Check the last committer in the branch provided by api
        :param branch: Required dict: Bitbucket REST API branch data
        :return: boolean
        """
        committer_info = branch["metadata"][BRANCH_INFO_LATEST_COMMIT]['committer']
        
        return committer_info['name']

    def branch_last_committer_email(self, branch):
        """
        Check the last committer in the branch provided by api
        :param branch: Required dict: Bitbucket REST API branch data
        :return: boolean
        """
        committer_info = branch["metadata"][BRANCH_INFO_LATEST_COMMIT]['committer']
        
        return committer_info['emailAddress']

    def branch_is_not_ahead(self, branch):
        """
        Check if the branch is (not) ahead of base branch
        :param branch: Required dict: Bitbucket REST API branch data
        :return: boolean
        """
        ahead_behind_info = branch["metadata"][BRANCH_INFO_AHEAD_BEHIND]
        # The branch has no additional commits comparing to base branch
        # (merged and no ongoing work)
        return int(ahead_behind_info["ahead"]) == 0

    def get_branch_head_age_days(self, branch):
        """
        Get branch latest commit age in days
        :param branch: Required dict: Bitbucket REST API branch data
        :return: int
        """
        br_head_data = branch["metadata"][BRANCH_INFO_LATEST_COMMIT]
        latest_commit_time = br_head_data["authorTimestamp"]
        br_head_age_days = timedelta(
            milliseconds=(time() * 1000 - int(latest_commit_time))).days
        logger.debug("Branch {}, last commit: {} day ago".format(
            branch["displayId"], br_head_age_days))

        return br_head_age_days

    def delete_old_branches(self):
        """
        Iterate through the old branches found and delete them if dry-run
        is not chosen
        """
        for old_branch in self.old_branches:
            logger.debug("Deleting branch: {}".format(old_branch["displayId"]))
            if not self.dry_run:
                if self.bitbucket.delete_branch(old_branch["id"]) == 400:
                    self.locked_branches.append(old_branch)
                    logger.info("Branch {} is locked from deletion. ".format(
                        old_branch["displayId"]))
                else:
                    self.bitbucket.delete_branch(old_branch["id"])
            else:
                logger.info("Skipping {} deletion as dryrun option set".format(
                    old_branch["displayId"]))

    def branch_pr_activity_not_older_than_days(self, branch, days):
        """
        Deciding if branch don't have active prs last `older_than_days` days
        :param branch: Required dict: Bitbucket REST API branch data
        :param days: Required int: Number of days to be considered as obsolete
        :return: boolean
        """
        if BRANCH_INFO_OUTGOING_PR in branch["metadata"]:
            pr_meta = branch["metadata"][BRANCH_INFO_OUTGOING_PR]
            if "pullRequest" in pr_meta:
                if self.pr_last_activity_not_older_than_days(
                        pr_meta["pullRequest"], days):
                    logger.debug(
                        "Found PR not older {} days for branch: {}".format(
                            days, branch["displayId"]))
                    return True
            else:
                for pr in self.bitbucket.get_all_pull_requests(
                        at=branch["id"], state="all"):
                    if self.pr_last_activity_not_older_than_days(pr, days):
                        logger.debug(
                            "Found PR not older {} days for branch: "
                            "{}".format(days, branch["displayId"]))
                        return True
        return False

    def pr_last_activity_not_older_than_days(self, pr, days):
        """
        Deciding if provided pr is outdated. PR is  considered outdated if:
            - it is not OPENED
            - it is DECLINED more than `days` ago
            - it is MERGED
        :param pr:  Required dict: Bitbucket REST API pull-request metadata
        :param days: Required int: Number of days to be considered as obsolete
        :return: boolean
        """
        if pr["state"] == "OPENED":
            logger.debug("Found OPENED pull-request: {}, for {} branch".format(
                pr["id"], pr["fromRef"]["displayId"]))
            return True
        if pr["state"] == "DECLINED":
            pr_last_activity_date = pr["updatedDate"]
            pr_age_days = timedelta(
                milliseconds=(time() * 1000 - int(pr_last_activity_date))).days
            logger.debug(
                "PR: {} from {} branch updated {} days ago".format(
                    pr["id"], pr["fromRef"]["displayId"], pr_age_days))
            return pr_age_days < days
        return False


def main():
    """
    Main logic
    :return: None
    """
    try:
        logger.info("Old branch remover started.")
        parser = argparse.ArgumentParser()
        parser.add_argument("--project", "-p",
                            help='BitBucket Project key',
                            required=True)
        parser.add_argument("--repo", "-r",
                            help="Repository to look into.",
                            required=True)
        parser.add_argument("--url", "-b",
                            help="Bitbucket url.",
                            default="https://sourcecode01.de.bosch.com/",
                            required=False)
        parser.add_argument("--user", "-u",
                            help="Username to log in to Bitbucket as. "
                                 "If not specified, .netrc data is used",
                            required=False)
        parser.add_argument("--passw", "-pw",
                            help="Password to log in to bitbucket with. "
                                 "If not specified, .netrc data is used.",
                            required=False)
        parser.add_argument("--days", "-d",
                            help="Branches older than the specified number of "
                                 "days will be considered old.",
                            default=90, required=False, type=int)
        parser.add_argument("--days-merged", "-dm",
                            help="Number of days to keep merged branches",
                            default=30, required=False, type=int)
        parser.add_argument("--force", "-f",
                            help='Force delete branches without confirmation.',
                            default=False, action="store_true", dest='force')
        parser.add_argument("--dry-run", "-dr",
                            help="Do not produce real deletion. Just logging.",
                            default=False, action="store_true", dest='dry_run')
        parser.add_argument("--debug", action="store_true", default=False,
                            dest='debug', help='Debug logging mode enable')
        parser.add_argument('-l', '--log_file',
                            help="Full path to log file")
        args = parser.parse_args()

        if args.log_file:
            logger.debug("Setting log file handler to {0}".format(
                args.log_file))
            logFormatter = logging.Formatter(
                "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] "
                " %(message)s")
            fileHandler = logging.FileHandler(args.log_file)
            fileHandler.setFormatter(logFormatter)
            logger.addHandler(fileHandler)

        if args.debug:
            logger.setLevel(logging.DEBUG)

        branch_deleter = BranchDeleter(args.url, args.project, args.repo,
                                       args.user, args.passw, args.days,
                                       args.days_merged, args.force,
                                       args.dry_run)
#        branch_deleter.delete()
        branch_deleter.mail()
    except Exception:
        if logger is not None:
            logger.exception(
                'Exception caught at top level, Process failed')
            sys.exit(1)
        else:
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
