import sys
import os

script_dir_path = os.path.dirname(os.path.abspath(__file__))

"""Import of JFrog REST API lib"""
from rest_api_lib import JfrogRESTApiLib

if __name__ == "__main__":

    url = sys.argv[1] 
    token = sys.argv[2] 
    artifact_to_be_downloaded = sys.argv[3] 
    destination_path = sys.argv[4]
    save_as_file_name = sys.argv[5]
    headers = {
            "Content-Type": "text/plain",
            "Authorization": f"Bearer {token}"
    }


    jfrog_api_lib = JfrogRESTApiLib(url, token)

    if jfrog_api_lib.get_availability() != True:
        print("Jfrog artifactory not available...")
        sys.exit(1)

    if os.path.exists(destination_path + save_as_file_name):
        print("File already exists...")
        print("Checking integrity of the existing file...")
        sha256_file_hash = jfrog_api_lib.get_sha256(destination_path + save_as_file_name)
        result_flag, file_info = jfrog_api_lib.get_file_info(artifact_to_be_downloaded)
        if (result_flag == True and sha256_file_hash == file_info.get_checksums_sha256()):
            print("File is valid...")
            sys.exit(0)
        else:
            print("File is invalid or something went wrong...")
            sys.exit(1)
        
    jfrog_api_lib.retrieve_artifact(artifact_to_be_downloaded, destination_path, save_as_file_name)