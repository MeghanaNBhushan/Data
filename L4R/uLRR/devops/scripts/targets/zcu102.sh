
declare -A TARGET_SETTINGS=(
    ["PATH_DTG_ST"]="xilinx_artifacts/device-tree-xlnx/device-tree-xlnx-xilinx_v2021.2.zip"
    ["PATH_DTG"]="$1/device-tree-xlnx-xilinx_v2021.2.zip"
    ["PATH_XSA_FILE"]="/ws/software/os/debian/hw/zcu102/system.xsa"
    ["PATH_U_BOOT_ST"]="xilinx_artifacts/u-boot-xlnx/u-boot-xlnx-xilinx-v2021.2.zip"
    ["PATH_U_BOOT"]="$1/u-boot-xlnx-xilinx-v2021.2.zip"
    ["PATH_BITSTREAM"]="/ws/software/os/debian/components/hw/build/build_zcu102/xsa/project_1.bit"
    ["PATH_KERNEL_ST"]="xilinx_artifacts/linux-xlnx/linux-xlnx-xilinx-v2021.2.zip"
    ["PATH_KERNEL"]="$1/linux-xlnx-xilinx-v2021.2.zip"
    ["PATH_R5_FW"]="/ws/software/os/debian/boot_bin/TmpR5App/uLRR.elf"
)

echo " - PATH_DTG_ST: ${TARGET_SETTINGS["PATH_DTG_ST"]}"
echo " - PATH_DTG: ${TARGET_SETTINGS["PATH_DTG"]}"
echo " - PATH_XSA_FILE: ${TARGET_SETTINGS["PATH_XSA_FILE"]}"
echo " - PATH_U_BOOT_ST: ${TARGET_SETTINGS["PATH_U_BOOT_ST"]}"
echo " - PATH_U_BOOT: ${TARGET_SETTINGS["PATH_U_BOOT"]}"
echo " - PATH_BITSTREAM: ${TARGET_SETTINGS["PATH_BITSTREAM"]}"
echo " - PATH_KERNEL_ST: ${TARGET_SETTINGS["PATH_KERNEL_ST"]}"
echo " - PATH_KERNEL: ${TARGET_SETTINGS["PATH_KERNEL"]}"
echo " - PATH_R5_FW: ${TARGET_SETTINGS["PATH_R5_FW"]}"