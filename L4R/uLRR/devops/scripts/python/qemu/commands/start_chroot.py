import click
import getpass
import os
import sys
from libs.rootfs_editor import RootFsEditor

# Define the start_chroot command
@click.command()
@click.option("--rootfs-filepath", help="Path to the rootfs.ext4 file", required=True)
@click.pass_context
def start_chroot(ctx, rootfs_filepath):
    """
    Start a chroot environment.

    Args:
        ctx (click.Context): The click context object.
        rootfs_filepath (str): Path to the rootfs.ext4 file.
    """

    # Check if the rootfs file exists
    if not os.path.exists(rootfs_filepath):
        # Rootfs file does not exist, handle the error
        click.echo(click.style(f"Error: Rootfs file '{rootfs_filepath}' does not exist.", fg="red"), file=sys.stderr)
        ctx.exit(1)

    # Start the chroot environment
    # Create an instance of the RootFsEditor class
    username = getpass.getuser()
    click.echo(click.style(f"Username: {username}", fg="green"))
    rootfs_editor = RootFsEditor(rootfs_filepath, username)
    rootfs_editor.mount_rootfs()

    rootfs_editor.start_chroot()
    click.echo(click.style("Chroot environment started successfully.", fg="green"))

    rootfs_editor = RootFsEditor(rootfs_filepath, username)
    rootfs_editor.unmount_rootfs()
    click.echo(click.style("Chroot environment stopped successfully.", fg="green"))
    