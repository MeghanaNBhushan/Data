#!/usr/bin/env python3
import json
import requests
import time
import logging

from modules.functions import *

# disable ssl warnings - we're inside the Bosch network,
# we trust self-signed certificates
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


class BitBucket:
    BITBUCKET_FETCH_LIMIT = 100  # max number of pages per request

    def __init__(self, url, project, repo, user, password):
        def get_bb_url(key):
            return urljoin(
                url, "rest", key, "1.0", "projects", project, "repos", repo)
        self.__url = get_bb_url("api")
        self.__branch_utils_url = get_bb_url("branch-utils")
        self.session = requests.session()
        if user and password:
            self.session.auth = (user, password)

        logger.debug("Created Bitbucket instance for {}".format(self.__url))

    def get_all_branches(self, details=False, order="MODIFICATION"):
        yield from self.__get_all_x(
            "branches", {"details": details, "order": order})

    def get_all_pull_requests(self, **kwargs):
        if not kwargs:
            params = {"state": "all"}
        else:
            params = kwargs
        yield from self.__get_all_x("pull-requests", params)

    def __get_all_x(self, key, params=None):
        """
        Getting all items from bitbucket e.g. all pull-requests.
        Parameters:
        :param key: type of elements to get e.g. "pull-requests"
        :param params: parameters to append to the URL as dict e.g.
        "{"state": "all"}"
        """
        page_counter = 0
        if params is None:
            params = {
                "start": page_counter,
                "limit": self.BITBUCKET_FETCH_LIMIT
            }
        else:
            params.update(
                {"start": page_counter, "limit": self.BITBUCKET_FETCH_LIMIT})
        logger.debug("Getting all {} with parameters: {}".format(key, params))
        req = None
        for attempt in range(5):
            req = self.session.get(
                url_param_join(urljoin(self.__url, key), params))
            if req.status_code == 429:
                logger.info(
                    "Error getting info (attempt {} of 5). Too many requests "
                    "to Bitbucket (Error code 429).".format(
                        page_counter, attempt + 1))
                time.sleep(5)
                continue
            elif req.status_code == 401:
                raise ConnectionError(
                    "Could not get {}. Unauthorized. Check your credentials "
                    "or .netrc file".format(key))
            elif req.status_code != 200:
                raise ConnectionError(
                    "Could not get {}. Status code: {} {}".format(
                        key, req.status_code, req.text))
            else:
                break
        while req.status_code == 200:
            br_data = req.json()
            page_counter += br_data["size"]
            logger.debug(
                "Getting elements {} - {} for key {}...".format(
                    page_counter, page_counter + br_data["size"], key))
            for br in br_data["values"]:
                yield br
            if br_data["isLastPage"]:
                break
            params["start"] = page_counter
            for attempt in range(5):
                req = self.session.get(
                    url_param_join(urljoin(self.__url, key), params))
                if req.status_code == 429:
                    logger.info(
                        "Could not get branches for elements {}+ "
                        "(attempt {} of 5) due to too many requests to "
                        "Bitbucket (Error code 429).".format(
                            page_counter, attempt + 1))
                    time.sleep(5)
                else:
                    break

    def delete_branch(self, br_id):
        """
        Delete remote branch
        :param br_id: Bitbucket branch id
        """
        for attempt in range(5):
            logger.info("Deleting branch #{}...".format(br_id))
            req = self.session.delete(
                urljoin(self.__branch_utils_url, "branches"),
                headers={
                    "X-Atlassian-Token": "no-check",
                    "Content-Type": "application/json"
                },
                data=json.dumps({"name": br_id, "dryRun": False}))
            if req.status_code == 204:
                logger.info("Branch {} was successfully deleted".format(br_id))
                return 204
            elif req.status_code == 429:
                # Wait and retry if Bitbucket blocked you due to too many
                # requests in a time
                logger.info(
                    "Could not delete branch {} (attempt {} of 5) "
                    "due to too many requests to Bitbucket "
                    "(Error code 429).".format(br_id, attempt + 1))
                time.sleep(5)
            elif req.status_code == 400:
                logger.debug(
                    "Branch {} is locked from deletion. "
                    "Response code: {}".format(br_id, req.status_code))
                return 400
            else:
                logger.warning(
                    "Branch {} could not be deleted. Response code: {}".format(
                        br_id, req.status_code))
                return req.status_code
