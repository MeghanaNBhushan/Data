import click
import getpass
import os
import sys
from libs.rootfs_editor import RootFsEditor


# Define the install_artifact command
@click.command()
@click.option("--artifact", help="Path to the artifact file", required=True)
@click.option("--destination-path", help="Path to the destination directory in the rootfs", required=True)
@click.option("--rootfs-filepath", help="Path to the rootfs.ext4 file", required=True)
@click.pass_context
def install_artifact(ctx, artifact, destination_path, rootfs_filepath):
    """
    Install an artifact into the rootfs file.

    Args:
        ctx (click.Context): The click context object.
        artifact (str): Path to the artifact file.
        destination_path (str): Path to the destination directory in the rootfs.
        rootfs_filepath (str): Path to the rootfs.ext4 file.
    """

    # Check if the artifact exists
    if not os.path.exists(artifact):
        # Artifact does not exist, handle the error
        click.echo(click.style(f"Error: Artifact '{artifact}' does not exist.", fg="red"), file=sys.stderr)
        ctx.exit(1)

    # Check if the rootfs file exists
    if not os.path.exists(rootfs_filepath):
        # Rootfs file does not exist, handle the error
        click.echo(click.style(f"Error: Rootfs file '{rootfs_filepath}' does not exist.", fg="red"), file=sys.stderr)
        ctx.exit(1)

    # Install the artifact
    # Create an instance of the RootFsEditor class
    username = getpass.getuser()
    click.echo(click.style(f"Username: {username}", fg="green"))
    rootfs_editor = RootFsEditor(rootfs_filepath, username)
    rootfs_editor.mount_rootfs() # Mount the rootfs file

    click.echo(click.style(f"Artifact: {artifact}", fg="green"))
    click.echo(click.style(f"Destination Path: {destination_path}", fg="green"))
    rootfs_editor.install_artifact(artifact, destination_path) # Install the artifact

    rootfs_editor.unmount_rootfs() # Unmount the rootfs file
    click.echo(click.style("Artifact installed successfully.", fg="green"))