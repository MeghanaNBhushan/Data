import subprocess
import os

def get_qemu_arch():
    # Replace this with your own logic to determine the QEMU architecture
    return "aarch64"

def check_binfmts_and_qemu():
    qemu_arch = get_qemu_arch()

    # Check and enable ARM emulation in kernel
    output = subprocess.run(["update-binfmts", "--display", f"qemu-{qemu_arch}"], capture_output=True, text=True)
    if "disabled" in output.stdout:
        print(f"qemu-{qemu_arch} not enabled")
        subprocess.run(["sudo", "update-binfmts", "--enable", f"qemu-{qemu_arch}"])
        output = subprocess.run(["update-binfmts", "--display", f"qemu-{qemu_arch}"], capture_output=True, text=True)
        if "disabled" in output.stdout:
            print(f"enable qemu-{qemu_arch} failed")
            return False
        else:
            print(f"enable qemu-{qemu_arch} successfully")

    # Check presence of qemu-aarch64-static
    if not os.path.isfile(f"/usr/bin/qemu-{qemu_arch}-static"):
        print(f"qemu-{qemu_arch}-static not found! Exiting.")
        return False

    # Check availability of debootstrap
    if not os.path.isfile("/usr/sbin/debootstrap"):
        print("debootstrap not found")
        return False

    return True