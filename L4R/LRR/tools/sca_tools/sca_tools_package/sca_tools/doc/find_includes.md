# <a name="find-includes-manual">Find Includes Manual</a>

Click [here](readme.md) to go back to the manual.

- [Find Includes Manual](#find-includes-manual)
  - [Purpose](#purpose)
    - [Role of Find Includes in Pull Request analysis](#role-of-find-includes-in-pull-request-analysis)
  - [Find Includes General Configuration](#find-includes-general-configuration)
    - [File Types Configuration](#file-types-configuration)
    - [File Filtering](#file-filtering)
      - [Customize search directories](#customize-search-directories)
      - [Exclusion mechanism](#exclusion-mechanism)
      - [Third Party Excludes](#third-party-excludes)
  - [Find source files which include header files](#find-source-files-which-include-header-files)
    - [Define Strategy for searching](#define-strategy-for-searching)
    - [Input Source Configuration](#input-source-configuration)
    - [Output Configuration](#output-configuration)
      - [Results Filtering](#results-filtering)
      - [Exporter Configuration](#exporter-configuration)
  - [Generate Headers to Source Mapping](#generate-headers-to-source-mapping)
    - [Publishing results to Standard Output](#publishing-results-to-standard-output)

## <a name="purpose">Purpose</a>

Find Includes allow to find all source files which include given header files.
The command supports 2 use cases:

- find all source files which include given header files
- generate mapping between source files and header files they include

### <a name="role-of-find-includes-in-pull-request-analysis">Role of Find Includes in Pull Request analysis</a>

Static code analysis tools (with or without help of SCA Tools) can run "lightweight" analysis only on selected files. But they accept only translation units for this purpose. Header files cannot be analyzed without translation units.

In order to be able to analyze header files it is necessary to identify source files which include modified header files (either all files which directly or indirectly include headers for full analysis, or at least one file for quick check).

Find Includes help to find all such source files and allow to implement solutions to run lightweight check of Pull Requests without necessity of running complete code analysis.

## <a name="find-includes-general-configuration">Find Includes General Configuration</a>

Parameters described in the section:

- `PROJECT_ROOT` - Path to the directory used by SCA Tools to resolve relative paths. Usually root of the repository.

The parameter sets root directory for find_includes functionality. All relative paths are resolved relative to this directory.

### <a name="file-types-configuration">File Types Configuration</a>

Parameters described in the section:

- `HEADER_EXTENSIONS` - List of header extensions to find includes from. By defaultdefault, is (".hpp", ".h", ".inl")
- `SOURCE_EXTENSIONS` - List of file extensions, to filter files that are considered for scan on 'include' directive of a header files given in input list

Find includes works with 2 file types: sources and headers.
By default, all files with extensions:

- ".hpp", ".h", ".inl" are considered as headers (can be included). It can be overridden via `HEADER_EXTENSIONS`
- ".cpp", ".c", ".inl" are considered as sources (can include). It can be overridden via `SOURCE_EXTENSIONS`

### <a name="file-filtering">File Filtering</a>

Find includes command supports several types of filtering files from processing and reporting.

#### <a name="customize-search-directories">Customize search directories</a>

Parameters described in the section:

- `CODE_DIRS_FILE` - Absolute path to a file that contains a list with folders (relative to the repo root) that should be scanned on includes.

By defaultdefault, all directories from `PROJECT_ROOT` except the '.git' are used to search source files.
The list of directories can be overridden via `CODE_DIRS_FILE` parameter if necessary.

#### <a name="exclusion-mechanism">Exclusion mechanism</a>

Parameters described in the section:

- `BLACKLIST_PATTERN` - Absolute path to a file that contains only one line with a pattern for the file blacklist pattern.

Find includes command filters out all the files whose names match the patterns from the specified list.

#### <a name="third-party-excludes">Third Party Excludes</a>

Parameters described in the section:

- `THIRDPARTY_PREFIXES` - Absolute path to a file that contains a list with 3rdparty prefixes to be excluded from the scan on includes.

If a file has prefix from the list specified via `THIRDPARTY_PREFIXES`, then it is considered as third party's one and not belonging to the source code to be scanned.

## <a name="find-source-files-which-include-header-files">Find source files which include header files</a>

By default, find_incudes look for translation units that directly or indirectly include given source file.
For more details refer to the sections below.

### <a name="define-strategy-for-searching">Define Strategy for searching</a>

Parameters described in the section:

- `FIND_INCLUDE_STRATEGY` - Specify how many c/cpp files with the given h/hpp/inl files included (directly or indirectly) to return. For "all" it returns a list of ALL c/cpp found. This is recommended when hpp/inl files contain C/C++ template code. For "minimal", a MINIMAL set of c/cpp is returned.

### <a name="input-source-configuration">Input Source Configuration</a>

Parameters described in the section:

- `FROM_LIST` - Read file list from specified input file. Otherwise, the list of source files is taken from the git diff of the current branch in the repository and its merge-base with origin/develop. Absolute or relative to repo root paths can be used.
- `FROM_STDIN` - Read file list from stdin. Otherwise, the file list is taken from git diff of the current branch in the repository and its merge-base with origin/develop.
- `MERGE_BASE` - Branch the diff is made against, default is origin/develop.

Find Includes command supports several ways to obtain list of files to search translation units for (in descending priority).

If `FROM_STDIN` is specified, then `find_includes` reads the list of files from standard input one by line.
If `FROM_LIST` is provided, then `find_includes` reads the list of files from the file specified.
If neither `FROM_STDIN` nor `FROM_LIST` are provided, then, by default, the command generates list of files using `git` utility by getting diff between `HEAD` and `origin/develop` branch. Branch name can be changed via `MERGE_BASE` parameter.

### <a name="output-configuration">Output Configuration</a>

The command support extra parameters to influence its output.

#### <a name="results-filtering">Results Filtering</a>

Parameters described in the section:

- `SOURCE_OUTPUT_EXTENSIONS` - List of file extensions, to filter files that are kept in a result output

The generated report contains translation units only with the extensions specified in the parameter.

#### <a name="exporter-configuration">Exporter Configuration</a>

Parameters described in the section:

- `OUTPUT_FILE` - The file path to write result list of source files to. Absolute or relative to repo root paths can be used.
- `TO_STDOUT` - Write results to stdout instead of file.

If `TO_STDOUT` is set to TrueTrue, then Find Includes will print the results to STDOUT.
OtherwiseOtherwise, the results will be written to the file specified in `OUTPUT_FILE`.

## <a name="generate-headers-to-source-mapping">Generate Headers to Source Mapping</a>

Parameters described in the section:

- `WITH_MAPPING_REPORT` - Changes find_includes behavior to generate a mapping headers to compilation units report. It accepts a path to the resulted report file.

If `WITH_MAPPING_REPORT` is specified, then `find_includes` command generate a report in Excel spreadsheet format with mapping of all header files found in `CODE_DIRS_FILE` directories to translation units which include them.

Filtering based on `THIRDPARTY_PREFIXES` value is enabled for mapping report generation

### <a name="publishing-results-to-standard-output">Publishing results to Standard Output</a>

Parameters described in the section:

- `TO_STDOUT` - Write mapping report to STDOUT

If `TO_STDOUT` is specified, then `find_includes` command additionally prints the report to standard output in the comma separated format: one header file and one translation unit per line. 