<!---

	Copyright (c) 2021 Robert Bosch GmbH and its subsidiaries.
	Copyright (c) 2009, 2018 Robert Bosch GmbH and its subsidiaries.
	This program and the accompanying materials are made available under
	the terms of the Bosch Internal Open Source License v4
	which accompanies this distribution, and is available at
	http://bios.intranet.bosch.com/bioslv4.txt

-->

# Release Note Generator (RnG) Roadmap

## Table of Contents

- [Planned Features](#planned)
- [Planned Features](#improve)
- [Known Limitations](#limitations)
- [Feature Requests](#requested)
- [Feature Request Template](#template)

## Planned Features <a name="planned"></a>

- **Splunk Data Input support**
    - user story (who/what/why):
    > As a developer I want to use splunk csv files as input data for QAC, Compiler, Resources, Coverity because it enables all projects to use the tool without minimzed project specific configuration/adaptions
    - more info: Splunk is standardized input data 
    - acceptance criteria:
        -  Draft stage support input of https://inside-docupedia.bosch.com/confluence/display/CCD/%5B5.1%5D+Data+Model


## Improvements/ <a name="improve"></a>

- [ ] Replace indidividal table creation functions such as generate_table_data, generate_compilerWarn_data into a generic table creation and table updating in adoc file
- [ ] Migrate jiraExport.ps1 from powershell to python to have common language used and to used commond logging mechanism
- [ ] Migrate asciidoc2htmlpdf.ps1 from powershell to python to have common language used and to used commond logging mechanism

## Known Limitations <a name="limitations"></a>

- [ ] If .logs folder does not exist python script does not work. Workaround. Create folder logs in root folder

## Feature Requests <a name="requested"></a>

Feel free to contact the [RnG maintainers](README.md#maintainers) if there is something that RnG could do to better cover your use case.

---

## Feature Request Template <a name="template"></a>

<!--
    user story:
    a one-sentence statement that very briefly describes your need
    It might help to think of it more as a newspaper headline than a legal statement or contract.
-->
<!--
    more info:
    Additional background info that further describes the request.
-->
<!--
    acceptance criteria:
    list of what lolli needs to allow you to do
-->

<!-- FEATURE REQUEST TEMPLATE: COPY, PASTE & FILL IN -->
- **FEATURE REQUEST: ..my feature..**
    - user story (who/what/why):
    > As *who* I need *what* in order to *why*.
    - more info:
    - acceptance criteria:
        - :white_check_mark: AC 1
        - :x: AC 2

---

<!---

	Copyright (c) 2021 Robert Bosch GmbH and its subsidiaries.
	Copyright (c) 2009, 2018 Robert Bosch GmbH and its subsidiaries.
	This program and the accompanying materials are made available under
	the terms of the Bosch Internal Open Source License v4
	which accompanies this distribution, and is available at
	http://bios.intranet.bosch.com/bioslv4.txt

-->