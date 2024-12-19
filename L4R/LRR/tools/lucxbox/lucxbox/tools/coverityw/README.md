# coverityw

-----------------------

The goal of this script is to simplify coverity usage in daily builds on a user machine or jenkins build scenarios.

Since coverity needs lots of parameters to run, the idea is to save these parameters in a file and use it as a way to simplify the command line used to build with coverity.

## Usage

```
usage: coverityw.py [-h] [-d] [-q] [--version]
                    [-s {all,configure,build,filter,analyze,commit}] -c
                    CONFIG_FILE -o OUTPUT_DIR -b BUILD_CMD [-u USER]
                    [-p PASSWORD]

Coverity configuration wrapper.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
  -s {all,configure,build,filter,analyze,commit}, --step {all,configure,build,filter,analyze,commit}
                        Coverity step to run
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Coverity configuration file
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Temporary directory for outputing coverity files
  -b BUILD_CMD, --build-cmd BUILD_CMD
                        Build command used to build the project
  -u USER, --user USER  User id that can publish to coverity server
  -p PASSWORD, --password PASSWORD
                        User password that can publish to coverity server
```

**Environment variables:**

* `COV_USER` - Set this environment variable with the user name, otherwise you must send the `-u` optional argument
* `COVERITY_PASSPHRASE` - Set this environment variable with the user password, otherwise you must send the `-p` optional argument

Examples:

```bash
python coverity.py -d -c "coverity-config.ini" -u "cya9abt" -p "pwdWithSpecialChars!$" -t "..\build_dir\new_temp_folder" -b "cmake ..\build_dir\. --other-args"
```

```bash
set COV_USER = "cya9abt"
set COVERITY_PASSPHRASE = "pwdWithSpecialChars!$"
python coverity.py -c "coverity-config.ini" -t "..\build_dir\new_temp_folder" -b "cmake ..\build_dir\. --other-args"
```

## Build command templates

For improving automation, the build command can contain the following keyword:

* `{COMPILER}` - This string (including the curly brackets) will be substituted by the full path of the compiler (including the exe name)
  
Example:

```bash
set COV_USER = "cya9abt"
set COVERITY_PASSPHRASE = "pwdWithSpecialChars!$"
python coverity.py -c "coverity-config.ini" -t "..\build_dir\new_temp_folder" -b "{COMPILER} file.cpp"
```

Will be interpreted as:

```bash
set COV_USER = "cya9abt"
set COVERITY_PASSPHRASE = "pwdWithSpecialChars!$"
python coverity.py -c "coverity-config.ini" -t "..\build_dir\new_temp_folder" -b "C:\TCC\Tools\mingw64\5.4.0_WIN64\bin\gcc.exe file.cpp"
```

## Powershell specifics

When using `powershell` instead of `cmd`, please change the `set` environment variable setter to the corresponding `$Env:<env_variable_name> = "<value>"`. Example:

```bash
$Env:COV_USER = "cya9abt"
$Env:COVERITY_PASSPHRASE = "pwdWithSpecialChars!$"
```

## Configuration file

This is an configuration file example, following the INI format:

```ini
###################################################
# Configure basic coverity attributes             #
###################################################
[COVERITY]

# Coverity bin full path (optional when running with TCC)
CoverityDir = C:\TCC\Tools\coverity\2018.03-1_WIN64\bin

# Compiler full path (optional when running with TCC)
CompilerPath = C:\TCC\Tools\mingw64\5.4.0_WIN64\bin\gcc.exe

# Server configuration
CoverityServerName = abts5364
CoverityPort = 8080
CoverityStreamName = coverity-example
CoverityAnalyzeOpts = --all

# Compiler config args (max 10 lines)
# Use the {COMPILER} macro to substitute it by the compiler full path
CompilerConfigArgs0 = --compiler=gcc --comptype gcc --template
# Examples of other configurations (green hills compiler)
# CompilerConfigArgs1 = --config path\specific_config.xml --compiler cxtri --comptype green_hills_cxx --xml-option append_arg:--ppp_translator --xml-option append_arg:"replace/\\|\\| defined\\(register\\)/|| 0" --template
# CompilerConfigArgs2 =  --config path\specific_config.xml --compiler cctri --comptype green_hills --xml-option append_arg:--ppp_translator --xml-option append_arg:"replace/\\|\\| defined\\(register\\)/|| 0" --template
# CompilerConfigArgs3 = ...
# CompilerConfigArgs4 = ...
# CompilerConfigArgs5 = ...
# CompilerConfigArgs6 = ...
# CompilerConfigArgs7 = ...
# CompilerConfigArgs8 = ...
# CompilerConfigArgs9 = ...

# Filter files from analysis (max 10 lines)
FilterFilePattern0 = .*iostream.*
# FilterFilePattern1 = .*/undesirable_module_a/.*
# FilterFilePattern2 = .*.undesirable_extension
# FilterFilePattern3 = .*/undesirable_file_name.*/
# FilterFilePattern4 = ...
# FilterFilePattern5 = ...
# FilterFilePattern6 = ...
# FilterFilePattern7 = ...
# FilterFilePattern8 = ...
# FilterFilePattern9 = ...

# Additional args when building
CoverityBuildAditionalArgs = --emit-complementary-info

#########################
## Integration with TCC #
#########################
[TCC]

# By marking this as true, get coverity and compiler path from tcc
UseTccTools = True

# Knowing just the compiler directory is not enough, we need more parameters
CompilerToolName = mingw64
CompilerRelativePath = bin\gcc.exe

# TCC XML configuration full path
TccScriptPath = C:\TCC\Base\InstallToolCollection\InstallToolCollection.ps1
TccXMLConfigPath = C:\TCC\Base\IF\Windows\TCC_IF_Windows_0.12.xml
TccInstallXML = True
TccInvoker = powershell
```

## Limitations

Althought the script can theoretically run on any system, TCC tools are officially, until now, only realeased to Windows. So TCC integration works only at Windows environments.