__copyright__ = """
@copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""
import sys
import os
import requests
import hashlib
import datetime

script_dir_path = os.path.dirname(os.path.abspath(__file__))

"""Import of Python Utils"""
python_utilities_path = os.path.abspath(os.path.join(script_dir_path, '../'))
sys.path.append(python_utilities_path)
from python_utilities import *

"""Import of auxiliar files"""
helper_files_path = os.path.abspath(os.path.join(script_dir_path, 'auxiliar/'))
sys.path.append(helper_files_path)
from folder_info_parser import *
from file_info_parser import *
from upload_in_chunks import *

# Console output switch
global g_verbose_mode
g_verbose_mode = True

class JfrogRESTApiLib:
    def __init__(self, base_url, token):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Object initialization: " + base_url + "; ", g_verbose_mode, "debug_mode")
        # Class member initialization
        
        self.base_url = base_url
        self.token = token

    def get_sha256(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path,"rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
            ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", sha256_hash.hexdigest(), g_verbose_mode, "debug_mode")

        return sha256_hash.hexdigest()

    def get_sha1(self, file_path):
        sha1_hash = hashlib.sha1()
        with open(file_path,"rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                sha1_hash.update(byte_block)
            ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", sha1_hash.hexdigest(), g_verbose_mode, "debug_mode")

        return sha1_hash.hexdigest()
    
    def get_md5(self, file_path):
        md5_hash = hashlib.md5()
        with open(file_path,"rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                md5_hash.update(byte_block)
            ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", md5_hash.hexdigest(), g_verbose_mode, "debug_mode")

        return md5_hash.hexdigest()

    def get_folder_info(self, folder_path):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Running: get_folder_info", g_verbose_mode, "debug_mode")
        # Description: Folder Info
        
        api_url = self.base_url + "/api/storage/" + folder_path
        ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " api_url: " + api_url, g_verbose_mode, "debug_mode")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        try:
            response = requests.get(api_url, headers=headers, timeout=5)
        except requests.exceptions.Timeout:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " The request timed out...", g_verbose_mode, "debug_mode")       
            return False
        folder_info_parser = FolderInfoParser(response.json())
        folder_info_parser.get_response()

        # check for success
        if response.status_code != 200:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " Something went wrong...", g_verbose_mode, "debug_mode")
            return False
        else:
            ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " Get folder info succeeded...", g_verbose_mode, "debug_mode")
            return True, folder_info_parser

    def get_file_info(self, file_path, uri=None):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Running: get_file_info", g_verbose_mode, "debug_mode")
        # Description: File Info
        
        if (uri == None):
            api_url = self.base_url + "/api/storage/" + file_path
        else:
            api_url = uri
        ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " api_url: " + api_url, g_verbose_mode, "debug_mode")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        try:
            response = requests.get(api_url, headers=headers, timeout=5)
        except requests.exceptions.Timeout:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " The request timed out...", g_verbose_mode, "debug_mode")       
            return False
        file_info_parser = FileInfoParser(response.json())

        # check for success
        if response.status_code != 200:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " Something went wrong...", g_verbose_mode, "debug_mode")
            return False
        else:
            ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " Get file info succeeded...", g_verbose_mode, "debug_mode")
            return True, file_info_parser

    def retrieve_artifact(self, file_path, destination_path, save_as_filename):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Running: retrieve_artifact", g_verbose_mode, "debug_mode")
        # Description: Returns an artifact from the specified destination.

        api_url = self.base_url + "/" + file_path

        headers = {
            "Content-Type": "application/octet-stream",
            "Authorization": f"Bearer {self.token}"
        }

        # Check if the folder exists
        if not os.path.exists(destination_path):
            # If it doesn't exist, create it
            os.makedirs(destination_path)
        
        save_as_file_path = destination_path + save_as_filename

        with open(save_as_file_path, "wb") as f:
            ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Downloading: " + save_as_file_path, g_verbose_mode, "debug_mode")
            try:
                response = requests.get(api_url, headers=headers, stream=True, timeout=5)
            except requests.exceptions.Timeout:
                ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " The request timed out...", g_verbose_mode, "debug_mode")       
                return False                
            total_length = response.headers.get('content-length')
            ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " status_code: " + str(response.status_code), g_verbose_mode, "debug_mode")

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]  %s MBytes/ %s MBytes" % ('=' * done, ' ' * (50-done), round(dl/(1024 * 1024), 3), round(total_length/(1024 * 1024), 3)) )    
                    sys.stdout.flush()
        print()

        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Calculating sha256 hash of the download file: " + save_as_file_path, g_verbose_mode, "debug_mode")
        sha256_file_hash = self.get_sha256(save_as_file_path)

        result_flag, file_info = self.get_file_info(file_path)
        if (result_flag == True and sha256_file_hash == file_info.get_checksums_sha256()):
            return True
        else:
            return False

    def create_directory(self, path_to_directory):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Running: create_directory", g_verbose_mode, "debug_mode")
        # Description: Create new directory at the specified destination.
        
        api_url = self.base_url + "/" + path_to_directory
        ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " api_url: " + api_url, g_verbose_mode, "debug_mode")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.put(api_url, headers=headers)

        # check for success
        if response.status_code != 201:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " Something went wrong...", g_verbose_mode, "debug_mode")
            return False
        else:
            ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " Create directory succeeded...", g_verbose_mode, "debug_mode")
            return True

    def deploy_artifact(self, path_to_artifact_source, path_to_artifact_dest):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Running: deploy_artifact", g_verbose_mode, "debug_mode")
        # Description: Deploy an artifact to the specified destination.

        api_url = self.base_url + "/" + path_to_artifact_dest
        ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " api_url: " + api_url, g_verbose_mode, "debug_mode")

        sha256_file_hash = self.get_sha256(path_to_artifact_source)
        sha1_file_hash = self.get_sha1(path_to_artifact_source)
        md5_file_hash = self.get_md5(path_to_artifact_source)

        headers = {
            "Content-Type": "application/octet-stream",
            "Authorization": f"Bearer {self.token}",
            "X-Checksum-Sha256": sha256_file_hash,
            "X-Checksum-Sha1": sha1_file_hash,
            "X-Checksum-MD5": md5_file_hash
        }

        response = requests.put(api_url, data=upload_in_chunks(path_to_artifact_source, chunksize=4096), headers=headers)

    
        # check for success
        if response.status_code != 201:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " Something went wrong...", g_verbose_mode, "debug_mode")
            return False
        else:
            ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " Deploy succeeded...", g_verbose_mode, "debug_mode")
            return True

    def delete_item(self, path_to_file_or_folder):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Running: delete_item", g_verbose_mode, "debug_mode")
        # Description: Deletes a file or a folder from the specified local repository or remote repository cache.

        api_url = self.base_url + "/" + path_to_file_or_folder
        ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " api_url: " + api_url, g_verbose_mode, "debug_mode")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.delete(api_url, headers=headers)

        # check for success
        if response.status_code != 204:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " Something went wrong...", g_verbose_mode, "debug_mode")
            return False
        else:
            ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " Delete action succeeded...", g_verbose_mode, "debug_mode")
            return True
        
    def get_artifacts_with_date_in_date_range(self, repo_key, from_val, to_val = int(datetime.datetime.now().timestamp() * 1000)):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Running: delete_item", g_verbose_mode, "debug_mode")
        # Description: Get all artifacts with specified dates within the given range. Search can be limited to specific repositories (local or caches).
        
        api_url = self.base_url + "/api/search/dates?from=" + str(from_val) + "&to=" + str(to_val) + "&repos=" + repo_key + "&dateFields=created"
        ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " api_url: " + api_url, g_verbose_mode, "debug_mode")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        try:
            response = requests.get(api_url, headers=headers, timeout=5)
        except requests.exceptions.Timeout:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " The request timed out...", g_verbose_mode, "debug_mode")       
            return False
        
        if response.status_code == 404:
            ConsoleOutput(bcolors.WARNING, "JfrogRESTApiLib", " Nothing to be deleted...!", g_verbose_mode, "debug_mode")
            return False

        for i in response.json()['results']:
            print(i)

        # check for success
        if response.status_code != 200:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " Something went wrong...", g_verbose_mode, "debug_mode")
            return False
        else:
            ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " Query succeeded...", g_verbose_mode, "debug_mode")
            return True
        
    def get_list_of_docker_tags(self, repo_key, image_name):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Running: get_list_of_docker_tags", g_verbose_mode, "debug_mode")
        # Description: Lists all tags of the specified Artifactory Docker repository.
        
        api_url = self.base_url + "/api/docker/" + repo_key + "/v2/" + image_name + "/tags/list"
        ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " api_url: " + api_url, g_verbose_mode, "debug_mode")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        try:
            response = requests.get(api_url, headers=headers, timeout=5)
        except requests.exceptions.Timeout:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " The request timed out...", g_verbose_mode, "debug_mode")       
            return False
        for i in response.json()['tags']:
            print(i)

        # check for success
        if response.status_code != 200:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " Something went wrong...", g_verbose_mode, "debug_mode")
            return False
        else:
            ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " Query succeeded...", g_verbose_mode, "debug_mode")
            return True
        

    def get_availability(self):
        ConsoleOutput(bcolors.OKBLUE, "JfrogRESTApiLib", " Running: get_availability", g_verbose_mode, "debug_mode")
        # Description: Sends a ping request
        
        api_url = self.base_url + "/api/system/ping"
        ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " api_url: " + api_url, g_verbose_mode, "debug_mode")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        try:
            response = requests.get(api_url, headers=headers, timeout=5)
        except requests.exceptions.Timeout:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " The request timed out...", g_verbose_mode, "debug_mode")       
            return False
        
        # check for success
        if response.status_code != 200:
            ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " Something went wrong...", g_verbose_mode, "debug_mode")
            return False
        else:
            if response.text == "OK":
                ConsoleOutput(bcolors.OKGREEN, "JfrogRESTApiLib", " Jfrog is alive...", g_verbose_mode, "debug_mode")
                return True
            else:
                ConsoleOutput(bcolors.FAIL, "JfrogRESTApiLib", " Jfrog is down...", g_verbose_mode, "debug_mode")
                return False