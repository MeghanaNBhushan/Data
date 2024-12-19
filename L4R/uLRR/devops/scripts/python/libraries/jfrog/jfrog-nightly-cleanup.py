import sys
import requests
import datetime
import warnings
import os

script_dir_path = os.path.dirname(os.path.abspath(__file__))

"""Import of JFrog REST API lib"""
from rest_api_lib import JfrogRESTApiLib


def parse_nightly_runs(folder_list: list) -> list:
    nightly_runs = [folder["uri"][1:] for folder in folder_list]
    return nightly_runs


def get_delete_date() -> str:
    date_today = datetime.date.today()
    date_two_week_ago = date_today - datetime.timedelta(days=14)

    return str(date_two_week_ago).replace("-","")


if __name__ == "__main__":

    url = "https://artifactory.boschdevcloud.com/artifactory"
    token = sys.argv[1] 
    headers = {
            "Content-Type": "text/plain",
            "Authorization": f"Bearer {token}"
    }

    jfrog_api_lib = JfrogRESTApiLib(url, token)

    if jfrog_api_lib.get_availability() != True:
        print("Jfrog artifactory not available...")
        sys.exit(1)
    
    result_flag, folder_info = jfrog_api_lib.get_folder_info("zugspitze-series-generic-local/nightly")

    if (result_flag == True):
        nightly_runs = parse_nightly_runs(folder_info.get_children())
        print("All nightly runs found in Artifactory:", nightly_runs, sep="\n")

        delete_date = get_delete_date()
        print(delete_date)

        for run in nightly_runs:
            if int(run.split("-")[0]) <= int(delete_date):
                print("Deleting run: " + run)
                result_flag = jfrog_api_lib.delete_item("zugspitze-series-generic-local/nightly/" + run)
                if result_flag != True:
                    warnings.warn(f"There might be a problem with the deletion of folder {run}")
                else:
                    print(f"Folder {run} is successfully deleted")

    else:
        print("Getting folder info without success...")
