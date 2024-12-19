""" Library for interface with bitbucket """

from datetime import datetime, timedelta
import json
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

LOGGER = logging.getLogger(__name__)


class PullRequest:
    def __init__(self, pr_id, title, created, closed, time_open, state, loc):
        self.pr_id = pr_id
        self.title = title
        self.created = created
        self.closed = closed
        self.time_open = time_open
        self.state = state
        self.loc = loc


# pylint: disable=too-many-locals
def get_prs(max_prs, project_name, repo, user, password, bitbucket_url, with_loc=False):
    """ Returns a list of pull request items """
    is_last_page = False
    pr_results = []
    start = 0

    while not is_last_page and start < max_prs:
        json_object = get_all_pull_requests(project_name, repo, user, password, start, bitbucket_url)
        for pull_request in json_object["values"]:
            if pull_request["toRef"]["displayId"] == "develop":
                try:
                    closed_date = int(pull_request["closedDate"]) / 1000
                    closed_date = datetime.utcfromtimestamp(closed_date).replace(microsecond=0)
                except KeyError:
                    closed_date = datetime.now() + timedelta(days=999)
                created_date = int(pull_request["createdDate"]) / 1000
                created_date = datetime.utcfromtimestamp(created_date).replace(microsecond=0)
                time_open = closed_date - created_date
                loc = 0
                if with_loc:
                    loc = get_loc(project_name, repo, user, password, pull_request["id"], bitbucket_url)

                pr_results.append(PullRequest(pull_request["id"], pull_request["title"],
                                              created_date, closed_date, time_open, pull_request["state"], loc))

        is_last_page = json_object["isLastPage"]
        if not is_last_page:
            start = json_object["nextPageStart"]

    return pr_results


def get_loc(project_name, repo, user, password, pr_id, bitbucket_url):
    try:
        session = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=1,
                        status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        diff_url = bitbucket_url + "/rest/api/1.0/projects/" + project_name + "/repos/" + repo + "/pull-requests/" + str(
            pr_id) + "/diff"
        response = session.get(diff_url, auth=(user, password), headers={'Accept-Encoding': 'identity'})
        json_object = json.loads(response.content)
        if json_object["truncated"]:
            return 10000
        else:
            return count_loc(json_object["diffs"])
    except (requests.exceptions.ChunkedEncodingError, KeyError) as exception:
        LOGGER.warning("Exception while calculating loc for PR-%s. (%s)", str(pr_id), str(exception))
        return 0
    except json.JSONDecodeError as decode_error:
        LOGGER.warning("Exception while calculating loc for PR-%s. Result might be too big to handle. (%s)",
                       pr_id["id"], str(decode_error))
        return 0


def count_loc(diffs):
    loc = 0
    for diff in diffs:
        if "binary" in diff:
            continue

        for hunk in diff["hunks"]:
            for segment in hunk["segments"]:
                if segment["type"] != "CONTEXT":
                    for _ in segment["lines"]:
                        loc = loc + 1
    return loc


def get_all_pull_requests(project_name, repo, user, password, start, bitbucket_url):
    response = requests.get(bitbucket_url + "/rest/api/1.0/projects/" + project_name +
                            "/repos/" + repo + "/pull-requests?" + "state=ALL&limit=100&start=" + str(start),
                            auth=(user, password))
    return json.loads(response.content)
