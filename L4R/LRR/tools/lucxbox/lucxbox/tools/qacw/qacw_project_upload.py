"""
QAC Project upload
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog, lucxutils
from lucxbox.tools.qacw import prqa_installation

LOGGER = lucxlog.get_logger()


def upload_qav(project_name, stream, snapshot, upload_source, url, username, password, path_prqa):
    """
    Method to upload the report to QAV

    :param project_name: The name of the project
    :param stream: The stream name
    :param snapshot: The snapshot name
    :param upload_source: Whether to upload source code as well or not ['ALL', 'ONLY_NOT_VCS', 'NONE']
    :param url: The url of the QAVerify server
    :param username: The username for the login to the QAVerify server
    :param password: The password
    :param path_prqa: The path to the PRQA executable
    """
    prqa = prqa_installation.PrqaInstallation(path_prqa)

    LOGGER.info("Uploading report to QAV")
    cmd_qav_upload = "{0} upload -P {1} --qav-upload " \
                     "--upload-project {2} " \
                     "--snapshot-name {3} " \
                     "--upload-source {4} " \
                     "--url {5} " \
                     "--username {6} " \
                     "--password {7}" \
        .format(prqa.cli, project_name, stream, snapshot, upload_source, url, username, password)
    out, err, code = lucxutils.execute(cmd_qav_upload)
    if code != 0:
        upload_cmd_wo_creds = "{0} upload -P {1} --qav-upload " \
                              "--upload-project {2} " \
                              "--snapshot-name {3} " \
                              "--upload-source {4} " \
                              "--url {5} " \
                              "--username ***** " \
                              "--password *****" \
            .format(prqa.cli, project_name, stream, snapshot, upload_source, url)
        LOGGER.critical("Command '%s' exited with code %s", upload_cmd_wo_creds, code)
        LOGGER.critical("With error: '%s'", err)
        LOGGER.critical("with output: '%s'", out)
        sys.exit(-17)


def upload_s101(project_name, path_prqa):
    """
    Method to upload the report to S101

    :param project_name: The name of the project
    :param path_prqa: The path to the PRQA executable
    """
    prqa = prqa_installation.PrqaInstallation(path_prqa)

    LOGGER.info("Uploading report to S101")
    s101_path = project_name + "/S101"
    if not os.path.exists(s101_path):
        os.mkdir(s101_path)

    cmd_s101 = "{0} upload -P {1} --s101-upload -u {2}".format(prqa.cli, project_name, s101_path)
    out, err, code = lucxutils.execute(cmd_s101)
    if code != 0:
        LOGGER.critical("Command '%s' exited with code %s", cmd_s101, code)
        LOGGER.critical("With error: '%s'", err)
        LOGGER.critical("with output: '%s'", out)
        sys.exit(-18)
