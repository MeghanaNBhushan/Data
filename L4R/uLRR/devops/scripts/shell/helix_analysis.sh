#!/bin/bash
# This script automates the setup and execution of static code analysis using Helix QAC for specified build directories and contexts.
# It executes a series of QAC commands to set licenses, check configurations, synchronize, analyze the code, and generate a SARIF report.
# Usage:
#   ./script_name.sh [build_directory_name] [build_context]
# Arguments:
#   build_directory_name - The target architecture directory (e.g., x86-64, armv8)
#   build_context - The build context (e.g., build_bl for business logic, build_aos_runnable for AOS runnable)

set -e
build_directory_name="$1"  # The build directory (x86-64 or armv8)
build_context="$2"         # The build context (build_bl or build_aos_runnable)
middleware_instance="$3"   # The middleware instance (e.g., te0950_neutrino)

echo "#################################################################"
echo "Build Directory Name: $build_directory_name"
echo "Build Context Name: $build_context"
echo "Middleware Instance: $middleware_instance"
echo -e "#################################################################\n"

# Set environment variables
export QAC_PROJECT_PATH="$(pwd)/tools/code_analysis/helix_qac/helix/l4_business_logic_gcc_lx"
export QAC_BIN_PATH="/opt/Perforce/Helix-QAC-2023.2/common/bin"
CONFIG_BASE_PATH="$QAC_PROJECT_PATH/prqa/configs/Initial/config"

echo "#################################################################"
case "$build_directory_name" in
    "x86-64")
        case "$build_context" in
            "build_bl") src_path="build/bl_linux_x86_64_debug/compile_commands.json" ;;
            "build_aos_runnable") src_path="build/aos_linux_x86_64_debug/compile_commands.json" ;;
            *) echo "Invalid build context: $build_context"; exit 1 ;;
        esac
        ;;
    "armv8")
        if [ "$middleware_instance" == "te0950_neutrino" ]; then
            case "$build_context" in
                "build_bl") src_path="build/bl_neutrino_armv8_debug/compile_commands.json" ;;
                "build_aos_runnable") src_path="build/aos_neutrino_armv8_debug/compile_commands.json" ;;
                *) echo "Invalid build context: $build_context"; exit 1 ;;
            esac
        else
            case "$build_context" in
                "build_bl") src_path="build/bl_linux_armv8_debug/compile_commands.json" ;;
                "build_aos_runnable") src_path="build/aos_linux_armv8_debug/compile_commands.json" ;;
                *) echo "Invalid build context: $build_context"; exit 1 ;;
            esac
        fi
        ;;
    *)
        echo "Unknown build directory name: $build_directory_name"; exit 1 ;;
esac

echo "Copying compile_commands.json from $src_path..."
cp "$src_path" .
cp "$QAC_PROJECT_PATH/../../sca_tools/l4_business_logic.json" .

echo -e "#################################################################\n"

# Update the JSON configuration file with absolute paths directly
jq --arg config_base_path "$CONFIG_BASE_PATH" --arg root_path "$(pwd)" '
    .ACF_FILE |= map($config_base_path + "/" + .) |
    .VCF_FILE = $config_base_path + "/" + .VCF_FILE |
    .RCF_FILE |= map($config_base_path + "/" + .) |
    .COMPILER_LIST |= map($config_base_path + "/" + .) |
    .USER_MESSAGES |= map($config_base_path + "/" + .) |
    .QAC_SYNC_PATH_BLACKLIST |= map($root_path + "/" + .) |
    .QAC_ANALYSIS_PATH_BLACKLIST |= map($root_path + "/" + .)
' l4_business_logic.json > l4_business_logic.json.tmp && mv l4_business_logic.json.tmp l4_business_logic.json
echo "Modified l4_business_logic.json:"
echo "#################################################################"

# Execute QAC set-license, check, setup, sync, and analyze commands
echo "QAC Analysis Started..."
qacli admin --set-license-server 5065@rb-lic-prqa-cloud.bosch.tech
qacli admin --check-license

# Function to perform sync, analyze, and generate reports
echo "Running QAC setup..."
sca_tools qac setup --qac_bin_path="$QAC_BIN_PATH" --qac_project_path="$QAC_PROJECT_PATH" -dp=l4_business_logic.json || true

echo "Running QAC sync..."
sca_tools qac sync --qac_bin_path="$QAC_BIN_PATH" --qac_project_path="$QAC_PROJECT_PATH" -dp=l4_business_logic.json || true

attempt_qac_analyze() {
    echo "Running QAC analyze..."
    sca_tools qac analyze --qac_bin_path="$QAC_BIN_PATH" --qac_project_path="$QAC_PROJECT_PATH" -dp=l4_business_logic.json
}

max_retries=2
retry_delay=5
attempt=1

while [ $attempt -le $max_retries ]; do
    echo "Attempt $attempt to perform analyze..."
    if attempt_qac_analyze; then
        echo "QAC Analysis successful."
        break
    else
        echo "Failed to analyze reports. Retrying in $retry_delay seconds..."
        sleep $retry_delay
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_retries ]; then
    echo "Failed to generate reports after $max_retries attempts."
    exit 1
fi

echo "Generating CSV report...."
sca_tools qac export_analysis --qac_bin_path="$QAC_BIN_PATH" --qac_project_path="$QAC_PROJECT_PATH" -dp=l4_business_logic.json --project_root="$(pwd)" --export_format="csv" --qac_logging_level="INFO" --ignore_failures --with_analysis --with_summary

echo "Generating SARIF report..."
qacli view -P "$QAC_PROJECT_PATH/" -t SARIF -m JSON --output-name helixqac || true

echo -e "\n#################################################################"
echo "Helix QAC analysis process completed."
echo -e "#################################################################\n"
