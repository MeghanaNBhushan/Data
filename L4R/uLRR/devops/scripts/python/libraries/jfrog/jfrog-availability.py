import sys
import os

script_dir_path = os.path.dirname(os.path.abspath(__file__))

"""Import of JFrog REST API lib"""
from rest_api_lib import JfrogRESTApiLib

if __name__ == "__main__":

    url = sys.argv[1] 
    token = sys.argv[2] 
    headers = {
            "Content-Type": "text/plain",
            "Authorization": f"Bearer {token}"
    }

    jfrog_api_lib = JfrogRESTApiLib(url, token)

    if jfrog_api_lib.get_availability() != True:
        print("Jfrog artifactory not available...")
        sys.exit(1)