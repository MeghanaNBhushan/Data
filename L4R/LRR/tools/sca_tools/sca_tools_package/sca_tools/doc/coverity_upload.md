# <a name="coverity-upload-manual">Coverity Upload Manual</a>

Click [here](readme.md) to go back to the manual.

- [Coverity Upload Manual](#coverity-upload-manual)
  - [Upload](#upload)
    - [Common Parameters Overview](#common-parameters-overview)

## <a name="upload">Upload</a>

*NOTE: Prior to upload analysis data Coverity Project must be analyzed with `coverity analyze` command.*

Coverity upload is done by `coverity upload` command.
SCA Tools uploads analysis report and source data to the Coverity Connect database in a specified stream.

SCA Tools save log file of the `coverity upload` command to `HELPER_LOGS_PATH/sca_tools_coverity_upload_{{datetime}}.log` file.

### <a name="common-parameters-overview">Common Parameters Overview</a>

Parameters described in the section:

- `COVERITY_USERNAME` - Username provided to access Coverity Connect server. Used in conjunction with the password. Must be provided as an environment variable
- `COVERITY_PASSWORD` - Password provided to access Coverity Connect server. Used in conjunction with the username. Must be provided as an environment variable
- `COVERITY_COMMIT_URL` - Use this option to specify the information needed to connect to a Coverity Connect server
- `COVERITY_COMMIT_HOST` - Name of the server without protocol. DEPRECATED, keeping for compatibility reasons. Use `COVERITY_COMMIT_URL` instead
- `COVERITY_COMMIT_DATAPORT` - Network TCP Port to be used while transferring data. DEPRECATED, keeping for compatibility reasons. Use `COVERITY_COMMIT_URL` instead
- `COVERITY_COMMIT_STREAM` - Stream name to which to commit the defects