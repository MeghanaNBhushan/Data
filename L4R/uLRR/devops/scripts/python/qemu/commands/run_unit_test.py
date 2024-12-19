import click
import getpass
import os
import sys
from libs.rootfs_editor import RootFsEditor


# Define the run_unit_test command
@click.command()
@click.option("--test-report-path", help="Path to where the test report will be stored", required=True)
@click.option("--rootfs-filepath", help="Path to the rootfs.ext4 file", required=True)
@click.pass_context
def run_unit_test(ctx, test_report_path, rootfs_filepath):
    """
    Run a unit test on the rootfs file.

    Args:
        ctx (click.Context): The click context object.
        test_report_path (str): Path to where the test report will be stored.
        rootfs_filepath (str): Path to the rootfs.ext4 file.
    """

    # Check if the rootfs file exists
    if not os.path.exists(rootfs_filepath):
        # Rootfs file does not exist, handle the error
        click.echo(click.style(f"Error: Rootfs file '{rootfs_filepath}' does not exist.", fg="red"), file=sys.stderr)
        ctx.exit(1)

    # Run the unit test
    # Create an instance of the RootFsEditor class
    username = getpass.getuser()
    click.echo(click.style(f"Username: {username}", fg="green"))    
    rootfs_editor = RootFsEditor(rootfs_filepath, username)
    rootfs_editor.mount_rootfs() # Mount the rootfs file

    click.echo(click.style(f"Test Report Path: {test_report_path}", fg="green"))
    rootfs_editor.run_unit_test(test_report_path) # Run the unit test

    rootfs_editor.unmount_rootfs() # Unmount the rootfs file
    click.echo(click.style("Artifact installed successfully.", fg="green"))