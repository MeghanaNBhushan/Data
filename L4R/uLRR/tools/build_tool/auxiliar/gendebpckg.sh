#!/bin/bash
set -e

# Script Name: gendebpckg.sh
# Author: C3 Team
# Description: This script generates a debian package.

cd $IR2_BUILD_TOOL_PATH
source auxiliar/print_colored_message.sh
source auxiliar/find_artefact.sh

function getarch(){
    local target_type="$1"

    # Define package architecture
    if [ "$target_type" == "x86-64" ]; then
        architecture="amd64"
    elif [ "$target_type" == "armv8" ]; then
        architecture="arm64"
    else
        print_colored_message "Error - Not expected target_type: $target_type" "$RED"
        exit 1
    fi
}

function buildpckgname() {
    local project="$1"
    local target_type="$2"
    local build_type="$3"

    local debian_revision_nr="1.0"

    architecture=""
    getarch $target_type

    # Extracting package name and version from the conan recipe - conanfile.py
    conan_recipe_path="conan_recipe_${project}"
    conan_recipe_file="${CONAN_SETTINGS[$conan_recipe_path]}/conanfile.py"
    package_name=$(grep -E "^\s*name\s*=\s*\"(.+)\"" "$conan_recipe_file" | sed -E 's/^\s*name\s*=\s*"(.+)"$/\1/')
    package_version=$(grep -E "^\s*version\s*=\s*\"(.+)\"" "$conan_recipe_file" | sed -E 's/^\s*version\s*=\s*"(.+)"$/\1/')

    # Build DEBIAN package name
    deb_package_name=${package_name//_/-}_${package_version}-${debian_revision_nr}_${architecture}
    print_colored_message "Creating deb. packg with the following name: $deb_package_name" "$GREEN"
}

function buildcontrolfile() {
    local deb_package_name="$1"
    local package_name="$2"
    local package_version="$3"

    architecture=""
    getarch $target_type
    
    cat > $deb_package_name/DEBIAN/control <<EOF
Package: ${package_name//_/-}-aos-runnable
Version: $package_version
Architecture: $architecture
Maintainer: "Imaging Radar - C3 Team <your.email@example.com>"
Description: "Imaging Radar - AOS runnables package"
Depends: libc6 (>= 2.31), libstdc++6 (>= 10.2.1), libgcc-s1 (>= 10.2.1)
EOF
}

function copyfolders() {
    local folder_names="$1"
    local pkg_base_folder="$2"
    local keep_path="$3"

    # Split the string into an array
    IFS=' ' read -r -a folder_names_array <<< "$folder_names"
    # Iterate through folder_names and create the same 
    for folder_name in "${folder_names_array[@]}"; do
        echo $folder_name        
        if [ -e "$folder_name" ]; then
            if [[ "$keep_path" == true ]]; then
                dest_path="$pkg_base_folder/$folder_name"
            else
                dest_path="$pkg_base_folder"
            fi
            # Create the folder if it doesn't exist
            mkdir -p "$dest_path"

            # Copy the artifacts
            cp -r $folder_name/* $dest_path
        fi
    done
}

function copyfiles() {
    local file_names="$1"
    local pkg_base_folder="$2"

    # Split the string into an array
    IFS=' ' read -r -a file_names_array <<< "$file_names"
    # Iterate through file_names and create the same
    for file_name in "${file_names_array[@]}"; do
        echo $file_name
        if [ -e "$file_name" ]; then
            # Copy the artifacts
            cp $file_name $pkg_base_folder
        fi
    done
}

function searchandcopyartefacts() {
    local file_names="$1"
    local dest_folder="$2"

    # Split the string into an array
    IFS=' ' read -r -a file_names_array <<< "$file_names"

    # Iterate through library_names and copy the same
    for file_name in "${file_names_array[@]}"; do
        artefact_path=""
        find_artefact $file_name
        library_path=$artefact_path

        if [ -n "$library_path" ]; then
            # Create the folder if it doesn't exist
            mkdir -p "$dest_folder"

            cp $library_path $dest_folder
        else
            echo "Missing shared library: $library_path"
            exit 1
        fi
    done    
}

# Function gendebpckg
function gendebpckg() {
    local project="$1"
    local os_type="$2"
    local target_type="$3"
    local build_type="$4"
    local middleware_instance="$5"

    source $IR2_BUILD_TOOL_PATH/config/settings.sh

    deb_package_name=""
    package_version=""
    package_name=""
    buildpckgname $project $target_type $build_type

    architecture=""
    getarch $target_type

    if [ "$target_type" == "x86-64" ]; then
        pkg_build_folder="build_x86_64/build_x86_64_exe"
    elif [ "$target_type" == "armv8" ]; then
        pkg_build_folder="build_armv8/build_armv8_exe"
    else
        echo "Unknown target type: $target_type"
        exit 1
    fi

    # Generate the package structure
    build_folder="build/${project}_${os_type}_${target_type}_${build_type}"
    pkg_base_folder="deb_package/$deb_package_name/opt/ulrr/usr/$pkg_build_folder"
    pushd $build_folder

        # Create the package structure
        mkdir -p "$pkg_base_folder"

        pushd "deb_package"
            # Create control script
            mkdir -p $deb_package_name/DEBIAN
            buildcontrolfile $deb_package_name $package_name $package_version
        popd

        #----------------------------------------------------------------------------------------------------------------
        # Fill the package with build files
        copyfolders "${DEB_PCKG_SETTINGS["build_folders_to_pckg"]}" $pkg_base_folder true

        # For armv8 deploy, add scripts to control the launch
        if [ "$target_type" == "armv8" ]; then
            copyfolders "${DEB_PCKG_SETTINGS["scripts_to_pckg"]}" "$pkg_base_folder/scripts" false
        fi 

        copyfiles "${DEB_PCKG_SETTINGS["diag_configs"]}" $pkg_base_folder true

        #----------------------------------------------------------------------------------------------------------------
        # If debug build_type, add additional files, that might be useful to know how the artefacts were built
        if [ $build_type = "debug" ]; then
            cp conanbuildinfo.json $pkg_base_folder/
            cp conaninfo.txt $pkg_base_folder/
            cp conan_run.log $pkg_base_folder/
            
            repo_url=$(git remote get-url origin)
            commit_hash=$(git rev-parse HEAD)
            current_branch=$(git rev-parse --abbrev-ref HEAD)
            cat > $pkg_base_folder/git_data <<EOF
Git-Repo: $repo_url
Git-Branch: $current_branch
Git-Hash: $commit_hash
EOF
        fi

        #----------------------------------------------------------------------------------------------------------------
        # To keep compatibility with existing testing framework, we need to provide means to discover the scripts
        if [ "$target_type" == "armv8" ]; then
            cat > $pkg_base_folder/scripts/setup_app_env.sh << EOF
#!/bin/bash
export IR2_MIDDLEWARE_INSTANCE="${middleware_instance}"
export START_ROUDI_SCRIPT="yaaac_codegen/deploy/carma_0_22/${middleware_instance}/start_scripts/start_${middleware_instance}.sh"
export STOP_ROUDI_SCRIPT="yaaac_codegen/deploy/carma_0_22/${middleware_instance}/stop_scripts/stop_${middleware_instance}.sh"

echo "IR2_MIDDLEWARE_INSTANCE: \$IR2_MIDDLEWARE_INSTANCE"
echo "START_ROUDI_SCRIPT: \$START_ROUDI_SCRIPT"
echo "STOP_ROUDI_SCRIPT: \$STOP_ROUDI_SCRIPT"
EOF
            sudo chmod +x $pkg_base_folder/scripts/setup_app_env.sh

            #----------------------------------------------------------------------------------------------------------------
            # Create symbolic link to the previous version of middleware instance        
            cat > "deb_package/$deb_package_name/DEBIAN/postinst" << EOF
#!/bin/sh
set -e

mkdir -p "/opt/ulrr/usr/build_armv8/build_armv8_exe/yaaac_codegen/deploy/carma_0_22/sensor/start_scripts"
ln -sf "/opt/ulrr/usr/build_armv8/build_armv8_exe/yaaac_codegen/deploy/carma_0_22/${middleware_instance}/start_scripts/start_${middleware_instance}.sh" "/opt/ulrr/usr/build_armv8/build_armv8_exe/yaaac_codegen/deploy/carma_0_22/sensor/start_scripts/start_sensor.sh"

exit 0
EOF
            sudo chmod +x deb_package/$deb_package_name/DEBIAN/postinst
        fi

        #----------------------------------------------------------------------------------------------------------------
        # Search for identified dependencies within AOS packages
        searchandcopyartefacts "${DEB_PCKG_SETTINGS["aos_shared_library"]}" "$pkg_base_folder/AOS/lib/"
        searchandcopyartefacts "${DEB_PCKG_SETTINGS["aos_tools"]}" "$pkg_base_folder/AOS/tools/"
        
        cat > $pkg_base_folder/AOS/update_paths.sh << EOF
#!/bin/bash
aos_libs_path="/opt/ulrr/usr/${pkg_build_folder}/AOS/lib"
aos_tools_path="/opt/ulrr/usr/${pkg_build_folder}/AOS/tools"

if [ -z "\$LD_LIBRARY_PATH" ]; then
    export LD_LIBRARY_PATH="\$aos_libs_path"
else
    export LD_LIBRARY_PATH="\$aos_libs_path:\$LD_LIBRARY_PATH"
fi

if [ -z "\$PATH" ]; then
    export PATH="\$aos_tools_path"
else
    export PATH="\$aos_tools_path:\$PATH"
fi

echo "LD_LIBRARY_PATH updated. New value: \$LD_LIBRARY_PATH"
echo "PATH updated. New value: \$PATH"
EOF
        sudo chmod +x $pkg_base_folder/AOS/update_paths.sh

        mkdir -p "$pkg_base_folder/scripts"

        cat > $pkg_base_folder/scripts/ir2_start_with_esme_example.sh << EOF
#!/bin/bash

export ROS_IP=192.168.2.16
export ROS_MASTER_URI=http://192.168.2.1:11311

export PYTHONPATH=\$PYTHONPATH:/usr/lib/python3.9/dist-packages/bsp_linux
export PYTHONPATH=\$PYTHONPATH:/usr/lib/python3.9/dist-packages/device_library

mount -o remount,size=2G /dev/shm

echo "Update LD_LIBRARY_PATH and PATH, to find AOS artefacts"
. /opt/ulrr/usr/$pkg_build_folder/AOS/update_paths.sh

# Execute the specified script
echo "Executing esme from 'root folder'"
cd /opt/ulrr/usr/$pkg_build_folder
esme yaaac_codegen/deploy/carma_0_22/${middleware_instance}/esme/esme_manifest_${middleware_instance}.json -1

EOF
        
        # Build DEBIAN package
        pushd "deb_package"
            echo $deb_package_name
            ls
            dpkg-deb --build --root-owner-group $deb_package_name
        popd
    popd
}