import click
import getpass
import os
import sys
from libs.rootfs_editor import RootFsEditor


# Define the install_deb command
@click.command()
@click.option("--deb-package", help="Path to the Debian package file", required=True)
@click.option("--rootfs-filepath", help="Path to the rootfs.ext4 file", required=True)
@click.pass_context
def install_deb(ctx, deb_package, rootfs_filepath):
    """
    Install a Debian package into the rootfs file.

    Args:
        ctx (click.Context): The click context object.
        deb_package (str): Path to the Debian package file.
        rootfs_filepath (str): Path to the rootfs.ext4 file.
    """

    # Check if the Debian package exists
    if not os.path.exists(deb_package):
        # Debian package does not exist, handle the error
        click.echo(click.style(f"Error: Debian package '{deb_package}' does not exist.", fg="red"), file=sys.stderr)
        ctx.exit(1)

    # Check if the rootfs file exists
    if not os.path.exists(rootfs_filepath):
        # Rootfs file does not exist, handle the error
        click.echo(click.style(f"Error: Rootfs file '{rootfs_filepath}' does not exist.", fg="red"), file=sys.stderr)
        ctx.exit(1)

    # Install the Debian package
    # Create an instance of the RootFsEditor class
    username = getpass.getuser()
    click.echo(click.style(f"Username: {username}", fg="green"))
    rootfs_editor = RootFsEditor(rootfs_filepath, username)
    rootfs_editor.mount_rootfs() # Mount the rootfs file

    click.echo(click.style(f"Debian Package: {deb_package}", fg="green"))
    rootfs_editor.install_deb_package(deb_package) # Install the Debian package

    rootfs_editor.unmount_rootfs() # Unmount the rootfs file
    click.echo(click.style("Debian package installed successfully.", fg="green"))