# User Manual for SCA Tools

This is a user manual for setting up the sca tools application.

### Helix QAC

| Use Case               | Document/Link                                                |
| ---------------------- | ------------------------------------------------------------ |
| Create a Project       | [sca_tools qac create](qac_create.md)                        |
| Analyze the Project    | [sca_tools qac analyze](qac_analyze.md)                      |
| Export Analysis        | [qac export_analysis](qac_export_analysis.md)                |
| QA Gate Filter         | [sca tools qac filter_qaview](qac_filter_qaview.md)          |
| Upload Results         | N.A. (QAVerify will be discontinued)                         |

### Coverity

| Use Case               | Document/Link                                                   |
| ---------------------- | --------------------------------------------------------------- |
| Create a Project       | [sca_tools coverity create](coverity_create.md)                 |
| Analyze the Project    | [sca_tools coverity analyze](coverity_analyze.md)<br/>[sca_tools coverity run_desktop](coverity_run_desktop.md)      |
| Export Report          | [sca_tools coverity export](coverity_export.md)                 |
| Preview Report         | [sca_tools coverity preview_report](coverity_preview_report.md) |
| QA Gate Filter         | N.A.                                                            |
| Upload Results         | [sca_tools coverity upload](coverity_upload.md)                 |

## Pull Request Gate (or Delta Analysis)

In C/C++ it is very often that changes will include only template and header files, which at Bosch takes usually the following forms:

* X.h: A C header file named X
* X.hpp/X.hxx: a C++ header file named X
* X.inl: A C++ header implementation file

These files they cannot be evaluated by tools directly as they do not generate object files directly in most cases, that is a .o, file. For evaluating these files with tools like Helix and Coverity, it is necessary to understand the impact on the actual source files **directly and indirectly** included as part of these changes. For this purpose, the SWQ team developed the [find_includes](find_includes.md) subcommand.

By integrating this command with a version control system (VCS) such as Git, it is possible to obtain a list of all the source files that should be rescanned as part of the Pull Request Gate for the project.

After the scan it is common to use the tool's generate report feature to identify in the outputs if the analysis includes high severity warnings.