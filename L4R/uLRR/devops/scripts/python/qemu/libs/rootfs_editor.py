__copyright__ = """
@copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""
import os
import sys
import pexpect
from pexpect_handler import PexpectHandler
from rich.console import Console


class RootFsEditor:
    def __init__(self, root_fs_file, default_cmd_prompt):
        """
        Initialize the RootFsEditor class.

        Args:
            root_fs_file (str): Path to the RootFS file.
            default_cmd_prompt (str): Default expected command line prompt.
        """
        # Class member initialization
        self.console = Console()
        
        # RootFS file
        self.root_fs_file = root_fs_file
        # Saving the default expected command line prompt
        self.default_cmd_prompt = default_cmd_prompt
        # Setup pexpect handler
        self.runner = PexpectHandler()

        self.console.print(f"[blue]RootFsEditor[/blue]: RootFS file: {self.root_fs_file}")
        self.console.print(f"[blue]RootFsEditor[/blue]: Default command prompt: {self.default_cmd_prompt}")


    def mount_rootfs(self):
        """
        Mount the RootFS file.

        Returns:
            bool: True if the RootFS is mounted successfully, False otherwise.
        """
        # Mount the RootFS file
        self.console.print(f"[blue]RootFsEditor[/blue]: Mount the RootFS file...")

        self.runner.command_request('sudo mkdir -p /mnt/rootfs', self.default_cmd_prompt)
        possible_answers = ['failed to setup', 'mounted on /mnt/rootfs', 'is already mounted', pexpect.EOF]
        returned_answer = self.runner.command_request('sudo mount --verbose -o loop ' + self.root_fs_file + ' /mnt/rootfs', possible_answers, 30)
        if returned_answer == 0:
            # 'failed to setup'
            self.console.print(f"[red]RootFsEditor[/red]: Failed to mount rootfs...")
            return False

        elif returned_answer == 1:
            # 'mounted on /mnt/rootfs'
            self.console.print(f"[green]RootFsEditor[/green]: Rootfs mounted with success!!!")
      
            self.runner.command_request('cd /mnt/rootfs', self.default_cmd_prompt)
            self.runner.command_request('ls', self.default_cmd_prompt)
            self.runner.command_request('sudo mount --verbose --bind /dev dev/', 'mount: /dev bound on /mnt/rootfs/dev')
            self.runner.command_request('sudo mount --verbose --bind /sys sys/', 'mount: /sys bound on /mnt/rootfs/sys')
            self.runner.command_request('sudo mount --verbose --bind /proc proc/', 'mount: /proc bound on /mnt/rootfs/proc')
            self.runner.command_request('sudo mount --verbose --bind /dev/pts dev/pts', 'mount: /dev/pts bound on /mnt/rootfs/dev/pts')
            self.runner.command_request('sudo cp /usr/bin/qemu-aarch64-static /mnt/rootfs/usr/bin', self.default_cmd_prompt)
            return True

        elif returned_answer == 2:
            # 'is already mounted'
            self.console.print(f"[red]RootFsEditor[/red]: Rootfs already mounted! Not expected!!!")
            user_input = input("Do you want to unmount the rootfs? (y/n): ")
            if user_input.lower() == "y":
                self.unmount_rootfs()
                self.mount_rootfs()
            else:
                self.console.print(f"[blue]RootFsEditor[/blue]: Rootfs will not be unmounted.")
                return False
      
        else:   
            # Unexpected behavior
            self.console.print(f"[red]RootFsEditor[/red]: Unexpected behavior!!!")
            print(self.runner.before)
            return False


    def unmount_rootfs(self):
        """
        Unmount the RootFS file.

        Returns:
            bool: True if the RootFS is unmounted successfully, False otherwise.
        """
        # Unmount the RootFS file
        self.console.print(f"[blue]RootFsEditor[/blue]: Unmount the RootFS file...")

        possible_answers = [pexpect.TIMEOUT, self.default_cmd_prompt, pexpect.EOF]
        returned_answer = self.runner.command_request('cd', possible_answers, 5)
        if returned_answer == 0:
            # Timeout
            self.console.print(f"[red]RootFsEditor[/red]: Timeout!!!")
            return False
        elif returned_answer == 1:
            # Default command prompt
            self.console.print(f"[blue]RootFsEditor[/blue]: Rootfs is mounted. Unmounting...")
        elif returned_answer == 2:
            # EOF
            self.console.print(f"[red]RootFsEditor[/red]: EOF!!!")
            return False
        
        self.runner.command_request('sudo umount --verbose /mnt/rootfs/dev/pts', 'umount: /mnt/rootfs/dev/pts unmounted')
        self.runner.command_request('sudo umount --verbose /mnt/rootfs/dev/', 'umount: /mnt/rootfs/dev/ unmounted')
        self.runner.command_request('sudo umount --verbose /mnt/rootfs/proc', 'umount: /mnt/rootfs/proc unmounted')
        self.runner.command_request('sudo umount --verbose /mnt/rootfs/sys', 'umount: /mnt/rootfs/sys unmounted')
        self.runner.command_request('sudo umount --verbose /mnt/rootfs/', 'umount: /mnt/rootfs/ unmounted')
        self.runner.command_request('sudo rm -rf /mnt/rootfs/', self.default_cmd_prompt)
        return True


    def start_chroot(self):
        """
        Start a chroot environment.

        Returns:
            bool: True if the chroot environment is started successfully, False otherwise.
        """
        # Start a chroot environment
        self.console.print(f"[blue]RootFsEditor[/blue]: Start chroot environment...")

        self.runner.command_request('sudo chroot /mnt/rootfs/ /bin/bash', 'root@')

        self.runner.interact()
        
        return True


    def install_artifact(self, artifact, destination_folder):
        """
        Install the given file or directory into the given destination folder.

        Args:
            artifact (str): Path to the file or directory to be installed.
            destination_folder (str): Destination folder to install the artifact.

        Returns:
            bool: True if the artifact is installed successfully, False otherwise.
        """
        # Install the given file into the given destination folder
        self.console.print(f"[blue]RootFsEditor[/blue]: Install artifact...")
        self.console.print(f"[blue]RootFsEditor[/blue]: Artifact: {artifact}")
        self.console.print(f"[blue]RootFsEditor[/blue]: Destination folder: {destination_folder}")


        if os.path.isdir(artifact):
            copy_command = 'mkdir -p  /mnt/rootfs' + destination_folder+ ' && sudo cp -r ' + artifact + ' /mnt/rootfs' + destination_folder
        elif os.path.isfile(artifact):
            copy_command = 'sudo cp ' + artifact + ' /mnt/rootfs' + destination_folder
        else:
            self.console.print(f"[red]RootFsEditor[/red]: The path is not a valid file or directory.")
            return False
    
        self.runner.command_request(copy_command, self.default_cmd_prompt)
        return True


    def install_deb_package(self, deb_pckg):
        """
        Install the given Debian package into the rootfs.

        Args:
            deb_pckg (str): Path to the Debian package.

        Returns:
            bool: True if the Debian package is installed successfully, False otherwise.
        """
        # Install the given Debian package into the rootfs
        self.console.print(f"[blue]RootFsEditor[/blue]: Install DEB package...")
        self.console.print(f"[blue]RootFsEditor[/blue]: DEB package: {deb_pckg}")
        self.runner.command_request('', self.default_cmd_prompt)

        # Upload deb package into the image
        self.runner.command_request('sudo cp ' + deb_pckg + ' /mnt/rootfs/home/', self.default_cmd_prompt)

        # Start chroot session
        self.runner.command_request('sudo chroot /mnt/rootfs/ /bin/bash', 'root@')

        # Install the DEB package
        path, filename = os.path.split(deb_pckg)
        self.runner.command_request("dpkg -i " + "home/"+filename, 'root@', 20)

        # Checking rpm package installation
        self.console.print(f"[blue]RootFsEditor[/blue]: Checking deb package: {deb_pckg}")

        self.runner.command_request('package_name_field=$(dpkg --info ' + "home/"+filename + ' | grep Package)', 'root@')
        self.runner.command_request('echo "$package_name_field"', 'root@')
        self.runner.command_request('package_name=$(echo "$package_name_field" | cut -d " " -f3)', 'root@')
        self.runner.command_request('echo "$package_name"', 'root@')

        self.runner.command_request('package_info=$(dpkg-query --status $package_name)', 'root@')
        self.runner.command_request('install_status=$(echo "$package_info" | awk "/^Status:/ {print $3}")', 'root@')

        possible_answers = ['is not installed and no information is available', 'install ok installed', pexpect.EOF]
        returned_answer = self.runner.command_request('echo $install_status', possible_answers, 20)
        if returned_answer == 0:
            # 'is not installed and no information is available'
            self.console.print(f"[red]RootFsEditor[/red]: DEB package not installed with success!!!")
            return False

        elif returned_answer == 1:
            # 'install ok installed'
            self.console.print(f"[green]RootFsEditor[/green]: DEB package installed with success!!!")
        
        else:   
            # Unexpected behavior
            self.console.print(f"[red]RootFsEditor[/red]: Unexpected behavior!!!")
            print(self.runner.before)
            return False

        # Clean-up, by removing *.deb file
        self.runner.command_request('rm -rf ' + "home/"+filename, 'root@')

        # Exiting chrooting
        self.runner.command_request('exit', self.default_cmd_prompt)

        return True


    def run_unit_test(self, test_reports_path, binary_path="/opt/ulrr/usr/build_armv8/build_armv8_exe/bin/"):
        """
        Run unit tests and save the test reports.

        Args:
            test_reports_path (str): Path to save the test reports.
            binary_path (str, optional): Path to the binary. Defaults to "/opt/ulrr/usr/build_armv8/build_armv8_exe/bin/".

        Returns:
            bool: True if the unit tests are run successfully and test reports are saved, False otherwise.
        """
        # Run unit test
        self.console.print(f"[blue]RootFsEditor[/blue]: Run unit test...")
        self.console.print(f"[blue]RootFsEditor[/blue]: Test reports path: {test_reports_path}")
        self.console.print(f"[blue]RootFsEditor[/blue]: Binary path: {binary_path}")

        # Start chroot session
        self.runner.command_request('sudo chroot /mnt/rootfs/ /bin/bash', 'root@')

        # Go to installation folder
        self.runner.command_request('cd ' + binary_path, 'root@')

        # Create folder for test reports
        self.runner.command_request('mkdir test_report', 'root@')

        # Update env PATHS
        self.runner.command_request('source /opt/ulrr/usr/build_armv8/build_armv8_exe/AOS/update_paths.sh', 'root@')

        # Runs unit-tests
        self.runner.command_request('find . -type f \( -name "*_test*" -a -executable \) -not -name "*esme*" -exec {} --gtest_output="xml:' + binary_path + 'test_report/" \;', 'root@')

        # Exiting chrooting
        self.runner.command_request('exit', self.default_cmd_prompt)

        # Copies the test reports to host, to be accessible to the outside
        self.runner.command_request('cp -r /mnt/rootfs' + binary_path + 'test_report/* ' + test_reports_path, self.default_cmd_prompt)

        return True
