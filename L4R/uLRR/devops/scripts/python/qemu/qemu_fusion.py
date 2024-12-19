"""
This script is used to rework IR2 rootfs. It provides commands for installing
Debian packages, installing artifacts, and running unit tests.

Usage:
    python qemu_fusion.py [command]

Commands:
    install-deb     Install a Debian package
    install-artifact    Install an artifact
    run-unit-test   Run unit tests
"""

__copyright__ = """
@copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""

import click
import os
import sys

tool_dir = os.path.dirname(os.path.realpath(__file__))
print(f"Tool directory: {tool_dir}")

tool_lib_dir = os.path.abspath(os.path.join(tool_dir, 'libs/'))
print(f"Tool library directory: {tool_lib_dir}")
sys.path.append(tool_lib_dir)

from commands.install_deb import install_deb
from commands.install_artifact import install_artifact
from commands.run_unit_test import run_unit_test
from commands.start_chroot import start_chroot

from libs.binfmts_qemu_checker import check_binfmts_and_qemu

@click.group()
@click.pass_context
@click.version_option()
def qemu_fusion(ctx):
    """
    QEMU Fusion is a tool for IR2 rootfs rework. It provides commands for
    installing Debian packages, installing artifacts, and running unit tests.
    """
    pass

qemu_fusion.add_command(install_deb)
qemu_fusion.add_command(install_artifact)
qemu_fusion.add_command(run_unit_test)
qemu_fusion.add_command(start_chroot)


if __name__ == '__main__':
    click.echo(click.style("", fg="green"))
    click.echo(click.style("Robert Bosch GmbH", fg="green"))
    click.echo(click.style("QEMU Fusion - IR2 Rootfs Rework Tool", fg="blue"))

    # Check and enable ARM emulation in kernel
    if not check_binfmts_and_qemu():
        sys.exit(1)

    # Start the tool
    qemu_fusion(obj={'tool_dir': tool_dir})

