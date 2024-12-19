# Release of the Static Code Analysis Tools

This document defines the guidelines, steps and commands to be executed for every release.

## Release authorized personnel

For the release of the SCA Tools check the [maintainers section in the readme](../readme.md#maintainers).

## Semantic Versioning

[Semantic Versioning](https://semver.org/) is a standard for release of software in a MAJOR.MINOR.PATCH format.

For the sca_tools the following additional meaning is given to each version:
- Major => API Changes and [CDF](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/cdf/browse) structural changes
- Minor => We release a new version based on our sprint chronogram – the minor checklist must be went through
- Patch => Hotfixes for versions – the patch checklist must be followed

## Creating the release branches

The first step to a release at the *start* of each release is to create a release branch according to the semantic version in the [CDF Board](https://rb-tracker.bosch.com/tracker/projects/CDF/summary). E.g. sca_tools_package X.Y.Z

### Release Development

All branches should be branched out to a release and in a timely manner be merged back to it before the tagging, if possible. 

The release of sca_tools_package and sca_tools should follow each accordingly the same steps

## Acceptance Criteria

The acceptance criteria for a release overall are given here.

### <a href="major_or_minor">For Major or Minor Release</a>

1. All Unit Tests are green.
  > This step is [currently CI integrated](https://rb-jmaas.de.bosch.com/ccad_doit_devops/job/software_quality/job/sca_helper_testsuite/).
  > Unit tests can be run with "python -m unittest" or "python run_tests.py -t unit" in the sca_tools directory.
2. No Pylint High priority issues and any of PEP8 warnings remain. This step is [currently CI integrated](https://rb-jmaas.de.bosch.com/ccad_doit_devops/job/software_quality/job/sca_helper_testsuite/).
  > This can be checked locally by runnung "python -m pylint" and "python -m pycodestyle" in the sca_tools directory.
3. All Integration Tests are green.
  > [SCA Mini-demo](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_mini_demo/browse) must be used for checking possible regressions with sca_tools_package – the currently released Helix QAC / Coverity versions should be tested here.
  > This step is [currently CI integrated](https://rb-jmaas.de.bosch.com/ccad_doit_devops/job/software_quality/job/sca_tools_integration_testsuite/) but the Jenkins job needs to be triggered manually. Be sure to provide the corresponding branch in "Build with Parameters".
  > Integration tests can be executed locally by runing "python test/integration/run_behave_tests.py" with all necessary arguments from the sca_tools directory.
4. The first three points must be checked for sca_tools release branch
5. The changelog.md must be updated on sca_tools with all CDF related ticket numbers and descriptions
  > Review the pull requests history to ensure that ALL release changes are covered. There is no automatic changelog generation mechanism.
6. sca_tools and sca_tools_package release must be approved and merged to develop. 
  > sca_tools should always be released first and the final merge branch merged to the same name release branch in sca_tools_package.
7. The develop itself should be then merged to master. 
  > This should happen both in sca_tools and sca_tools_package but there is a dependency between both of them. sca_tools should always be released first.
8. The master branch should be tagged
  > git tag -a vX.Y.Z -m "SCA TOOLS (PACKAGE) X.Y.Z" or directly in the web UI with Bitbucket
9. Synchronize modified CCT files (if any) with [prqa_qaf](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/prqa_qaf/browse) repository:
  > Create feature branch with sca_tools_package release branch name
  > Add modified CCT to the [cct](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/prqa_qaf/browse/config/cct) directory
  > Create Pull Request to the master branch
10. Submodule link to sca_tools_package in [sca_mini_demo](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_mini_demo/browse) should be updated

### For Patches

All the previous steps for [major and minor releases](#major_or_minor) apply plus the following:

11. Notify users of affected Tickets about the Patch (through CDF ticket)
  > Patches should only be created after critical bugs are found that can no longer wait for the regular release cycle to be handled.
12. Verify with the users if the patch successfully solved the ticket
  > User feedback is sine qua non to ensure a successful patch release. 

### Merging Pull Requests

Bitbucket provides [out of the box](https://zapier.com/apps/bitbucket/tutorials/bitbucket-pull-request) a merging mechanism. This mechanism should be used to create Pull requests from the steps. 

The same is true for [tagging](https://support.atlassian.com/bitbucket-cloud/docs/repository-tags/) after the merges to master are performed.

### Subtree in sca_tools_package

The [GIT subtree](https://www.atlassian.com/git/tutorials/git-subtree) is a mechanism to merge and maintain different git repository subtrees in a single repository and is supported in modern Git development. It is a versatile mechanism to avoid the [over usage of submodules and it's implications](https://codewinsarguments.co/2016/05/01/git-submodules-vs-git-subtrees/). 

The subtree configuration for sca_tools_package needs to be setup [sca_tools](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools/browse).
Run from the root of sca_tools_package "git remote add sca_tools ssh://git@sourcecode.socialcoding.bosch.com:7999/cdf/sca_tools.git"

Example output for "git remote -v" after remote repository configurations:
```
  origin      ssh://git@sourcecode.socialcoding.bosch.com:7999/cdf/sca_tools_package.git (fetch)
  origin      ssh://git@sourcecode.socialcoding.bosch.com:7999/cdf/sca_tools_package.git (push)
  sca_tools   ssh://git@sourcecode.socialcoding.bosch.com:7999/cdf/sca_tools.git (fetch)
  sca_tools   ssh://git@sourcecode.socialcoding.bosch.com:7999/cdf/sca_tools.git (push)
```

In this case, all changes from the subtrees can be replicated into the sca_tools_package with: 
  - git subtree pull --prefix=sca_tools sca_tools release/MyReleaseBranch

In each of these command the rules described in the official Git documentation apply and should be considered valid in the scope of it's usage.

## Update of Links and Notification

By executing this final step the consistency of the release is ensured. It consists of updating the technical changelogs and notifying the users of the key software changes of the iteration.

### Changelogs

After ensuring that all changes are "safe for usage", the changelogs for both sca_tools and sca_tools_package should contain the highlights of the changes performed by the development team.

### Notifications

After all the previous steps are concluded, the final steps are:

1. Update the [Docupedia Roadmap Page](https://inside-docupedia.bosch.com/confluence/display/CCD/Static+Code+Analysis#StaticCodeAnalysis-roadmap)
2. Notify client project integrators through e-mail, highlighting the main changes and linking out the changelogs.
