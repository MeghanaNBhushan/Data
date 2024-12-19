import subprocess
import tempfile
import colorama
import sys
import os

colorama.init()

# Tools that could be installed
def install_aos():

    def check_of_aos_repos():
        conan_remote_list = subprocess.Popen(["conan", "remote", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = conan_remote_list.communicate()
        for element in stdout.split():
            possible_repo = element.decode()[:-1]
            if possible_repo in list_of_unwanted_repos:
                commands.insert(0, ["conan", "remote", "disable", possible_repo])


    storage_account_url = "https://swbuildir2st.file.core.windows.net/a-core-application-container/"
    conan_config_v_2_49_file = "conan_config-v2.49.0.zip"
    conan_config_v_2_49_sas = "?st=2023-08-30T08%3A26%3A35Z&se=2031-08-31T08%3A26%3A00Z&sp=r&sv=2022-11-02&sr=f&sig=a9er1ryoObLG6uaCIFBYk%2F3S2KiQR71LOioMVD7%2BOJg%3D"
    temp_dir = tempfile.TemporaryDirectory()
    build_dir = temp_dir.name
    list_of_unwanted_repos = ["aos-release", "aos-staging", "aos-dev", "esi-sandbox", "conan-center-mirror", "aos-external-dependencies", "aos-deprecated-release-now-sandbox"]

    commands = [
        ["curl", f"{storage_account_url}{conan_config_v_2_49_file}{conan_config_v_2_49_sas}", "--output", conan_config_v_2_49_file],
        ["conan", "remove", "*/*@aos/*", "--force"],
        ["conan", "config", "install", f"{conan_config_v_2_49_file}"],
        ["conan", "remote", "update", "zugspitze-series-aos-18-local", "https://artifactory.boschdevcloud.com/artifactory/api/conan/zugspitze-series-aos-18-local", "--insert", "0"],
    ]

    # Add conan remote disable commands if it exists 
    check_of_aos_repos()

    # Create working direktory

    # Execute commands in subprocesses
    for command in commands:
        try:
            subprocess.run(command, cwd=build_dir, check=True)
        except subprocess.CalledProcessError as err:
            print(colorama.Fore.LIGHTRED_EX + f"\nError while executing {err}" + colorama.Fore.RESET)
            print(colorama.Fore.LIGHTRED_EX + "\nAOS may not be installed, please close devcontainer and reopen in local folder, remove the container and try again!" + colorama.Fore.RESET)
            os.system("echo 'export PS1=\"\\[\\033[31m\\] !!! No AOS - devcontainer broken !!! \\[\\033[0m\\] \\u@\\h:\\w$\"' >> ~/.bashrc")
            sys.exit(1)
    
if __name__ == "__main__":
    install_aos()


    


