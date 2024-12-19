#!/usr/bin/env python3
"""
Create Workon drafts and check of work on status


# What needs to be done on the production system
# Signed email fo project lead which confirms quality / testing is done
# System Name - must not change (Application Key is system specific)
# KeyID has to stay within project (confidental info)
# Boundery conditions have to be defined
# - Which REST apis are used, are multiple flows available.
# Contact points has to be mentioned

# Author: Jochen Held (XC-DA/EDB7)
"""

import os
import glob
import json
from base64 import b64encode
from pathlib import Path
import requests
import logging

logger = logging.getLogger(__name__)


WORKON_CFG = "workon_cfg.json"
BUILD_INFO = "build_info.json"

#####################################################
# Key and Endpoint are confidential
# they are stored in external json file WORKON_REST_CFG
######################################################
WORKON_REST_CFG = Path(__file__).parent.absolute().joinpath("workon_rest_cfg.json")


def workon_get_status(rest_cfg, request_id):
    """
    Calls the workon rest api to get status based on workon ID
    Args:
        rest_cfg: REST configuration including endpoint and key-id
        request_id: workon ID

    Return:

    """

    # Which status of workon exist
    # Resolution
    # unresolved: as long as workon is open and not all approvals availabe
    # canceled: creator of request canceled the workon
    # approved: all approves approved
    # declined: some of approves declined

    url = rest_cfg["rest_status"]["url"] + "/" + request_id
    key_id = rest_cfg["rest_status"]["key_id"]

    r = requests.get(
        url,
        headers={"KeyId": key_id},
    )

    # Server resonse 200 --> success, all other return codes means error
    if r.status_code == 200:
        r_data = r.json()
        logger.debug("WorkOnStatus - " + request_id + ": " + r_data["resolution"])
        return r_data["resolution"]
    else:
        logger.error("Error getting workon Status - Server resonse:  " + str(r))
        workon_key = None
        sys.exit(10)


def workon_create_draft(rest_cfg, request_data):
    """
    Calls the workon rest api to create a draft
    Args:
        rest_cfg: REST configuration including endpoint and key-id
        request_data: workon json string

    Return:
        request_data: return the json string with the attachments

    """

    url = rest_cfg["rest_draft"]["url"]
    key_id = rest_cfg["rest_draft"]["key_id"]

    r = requests.put(
        url,
        headers={
            "KeyId": key_id,
            "Content-Type": "application/json",
        },
        data=json.dumps(request_data),
    )

    # Server resonse 200 --> success, all other return codes means error
    if r.status_code == 200:
        r_data = r.json()
        workon_key = r_data["key"]
        logger.debug("Workon successfully created (Server response: " + str(r))
        logger.debug("Workon Key: " + workon_key)
    else:
        logger.error("Error creating work on. Server resonse:  " + str(r))
        workon_key = None
        sys.exit(10)

    return workon_key


def workon_add_attachments(rn_dir, request_data):
    """
    Fills in the text infos in the release note such as summary, comment
    Args:
        rn_dir: folder containing the workon json template (includes e.g. the approver list)
        request_data: workon json string

    Return:
        request_data: return the json string with the attachments

    """

    attachment = {"rbga.field.attach": []}
    request_data["data"].update(attachment)

    # To search for all PDF files ins release notes output folder
    for counter, file in enumerate(
        glob.glob(
            str(Path(rn_dir)) + "/**/*.pdf",
            recursive=True,
        )
    ):

        # Workon expects base64 encoded and utf-8 conform files
        with open(file, "rb") as pdf_file:
            pdfFileBase64_bytes = b64encode(pdf_file.read())

        pdfFileBase64_string = pdfFileBase64_bytes.decode("utf-8")

        fileinfo = {
            "filename": Path(file).name,
            "file": pdfFileBase64_string,
        }
        request_data["data"]["rbga.field.attach"].append(fileinfo)

    return request_data


def workon_fill_release_info(request_data, build_info):
    """
    Fills in the text infos in the release note such as summary, comment
    Args:
        request_data: folder containing the workon json template (includes e.g. the approver list)
        build_info: containts the build info json which is used to add additional infos to the workon

    Return:
        request_data: return the json string with the attachments

    """
    summary = (
        build_info["general_info"]["project"]["value"]
        + " - "
        + build_info["general_info"]["release_version"]["value"]
    )

    # description in workon dashboard
    request_data["summary"] = summary

    # short description (Kurzbeschreibung)
    request_data["data"]["rbga.field.description"] = summary

    # Compile the comment
    comment = "Hello everybody, \n\n Please sign following system release notes: \n \n"
    attachments = request_data["data"]["rbga.field.attach"]
    for attachment in attachments:
        comment = comment + attachment["filename"] + "\n"
    comment += "\nThank you!"

    # description (Beschreibung)
    request_data["data"]["rbga.field.comments"] = comment

    return request_data


def get_rest_cfg():
    # load the rest config with the confidental key information
    try:
        with open(Path(WORKON_REST_CFG), "r") as json_file:
            rest_cfg = json.load(json_file)
    except EnvironmentError:
        logger.error(
            "******************************************************\n"
            + "REST Config missing!!!!\n "
            + str(WORKON_REST_CFG)
            + "\n \nThe REST configuration containts the endpoint to\n"
            + "P or Q server and the api key. This data is confidential\n"
            + "and must not be shared!!!"
            + "\n******************************************************"
        )
        sys.exit(10)

    return rest_cfg


def sign_release_note(cfg_dir, rn_dir, build_dir):
    """
    Main function creating the workon json input including attachment and then calling
    REST api of workon to create the workon draft
    Args:
        cfg_dir: folder containint the workon json template (includes e.g. the approver list)
        rn_dir: contains the release note documents which are attached
        build_dir: containts the build info json which is used to add additional infos to the workon

    Return:
        workon_key: Workon ID of created draft

    """

    # load the workon rest json input template
    request_data = []
    with open(Path(cfg_dir).joinpath(WORKON_CFG), "r") as json_file:
        request_data = json.load(json_file)

    # load the build info data such project name, release name,...
    with open(Path(build_dir).joinpath(BUILD_INFO), "r") as json_file:
        build_info = json.load(json_file)

    # add the pdf attachments
    request_data = workon_add_attachments(rn_dir, request_data)

    # Update the release informations. This must be called after attaching the files
    request_data = workon_fill_release_info(request_data, build_info)

    rest_cfg = get_rest_cfg()

    # Create Workon
    workon_key = workon_create_draft(rest_cfg, request_data)

    return workon_key


def get_release_note_approval_status(key):

    rest_cfg = get_rest_cfg()

    workon_get_status(rest_cfg, key)


def main():

    build_dir = "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/build_data/"
    cfg_dir = "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/cfg/"
    rn_dir = "C:/Users/hej3lr/git/releasenotegenerator/src/signer/test/"

    sign_release_note(cfg_dir, rn_dir, build_dir)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main()
