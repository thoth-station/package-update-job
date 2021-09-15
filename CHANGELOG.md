# Changelog for Thoth's Template GitHub Project

## Release 0.8.12 (2021-09-15T04:38:57)
### Features
* Add harshad as a maintainer
* Update of the dependencies

## [0.1.0] - 2019-Sep-11 - goern

### Added

all the things that you see...

## Release 0.7.0 (2020-07-08T14:32:34)
* Update .thoth.yaml (#90)
* :pushpin: Automatic update of dependency pre-commit from 2.5.1 to 2.6.0 (#87)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.0 to 0.24.2 (#86)
* :sparkles: added the cyborg-supervisors team to prow univers, after we have had it as a github team
* :sparkles: added the cyborg-supervisors team to prow univers, after we have had it as a github team
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.2.9 to 0.3.0 (#84)
* :pushpin: Automatic update of dependency thoth-storages from 0.23.2 to 0.24.0 (#83)
* Create OWNERS
* :pushpin: Automatic update of dependency pre-commit from 2.4.0 to 2.5.1
* :pushpin: Automatic update of dependency thoth-python from 0.9.2 to 0.10.0
* :pushpin: Automatic update of dependency thoth-python from 0.9.2 to 0.10.0
* :pushpin: Automatic update of dependency pre-commit from 2.4.0 to 2.5.1
* :pushpin: Automatic update of dependency pre-commit from 2.4.0 to 2.5.1
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.23.2
* :pushpin: Automatic update of dependency thoth-storages from 0.22.12 to 0.23.2
* :pushpin: Automatic update of dependency pylint from 2.5.2 to 2.5.3
* :pushpin: Automatic update of dependency pytest from 5.4.2 to 5.4.3
* added a 'tekton trigger tag_release pipeline issue'
* :pushpin: Automatic update of dependency thoth-storages from 0.22.11 to 0.22.12
* hotfixing the __name__
* :pushpin: Automatic update of dependency thoth-storages from 0.22.10 to 0.22.11
* :pushpin: Automatic update of dependency thoth-storages from 0.22.9 to 0.22.10
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.2.7 to 0.2.9
* :pushpin: Automatic update of dependency pre-commit from 2.3.0 to 2.4.0
* :pushpin: Automatic update of dependency thoth-messaging from 0.3.5 to 0.3.6
* :pushpin: Automatic update of dependency pytest from 5.4.1 to 5.4.2
* :pushpin: Automatic update of dependency thoth-messaging from 0.3.4 to 0.3.5
* :pushpin: Automatic update of dependency pylint from 2.5.1 to 2.5.2
* :pushpin: Automatic update of dependency pylint from 2.5.0 to 2.5.1
* working with python module
* add self as maintainer
* move process message
* move to sub directory and add init file
* updated github templates
* updated
* :pushpin: Automatic update of dependency thoth-storages from 0.22.8 to 0.22.9
* add FAUST_DEBUG env
* :pushpin: Automatic update of dependency pylint from 2.4.4 to 2.5.0
* :pushpin: Automatic update of dependency thoth-storages from 0.22.7 to 0.22.8
* remove service account
* :pushpin: Automatic update of dependency pre-commit from 2.2.0 to 2.3.0
* :pushpin: Automatic update of dependency thoth-python from 0.9.1 to 0.9.2
* Correct errors
* hot fixing by removing a Q
* Add Route and correct port
* messages only present in messaging module
* Adjust module name in the header
* remove app.py
* Correct key for ConfigMap
* Bump pyyaml from 3.13 to 5.1
* use thoth config map for configuration
* Set client_id, remove unnecessary imports and variables
* remove backend and frontend namespaces
* Update ill formed piplock
* Fix errors in openshift templates
* remove local messaging implementation
* Use messaging module
* :green_heart: fixed coala errors
* :sparkles: added black and pytest and pylint, relocked, added .vscode/ to gitignore
* :green_heart: added some more standard project config files
* reformatting
* :sparkles: now with fresh precommitness
* :pushpin: Automatic update of dependency thoth-storages from 0.22.5 to 0.22.6
* :pushpin: Automatic update of dependency thoth-common from 0.12.3 to 0.12.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.12 to 0.12.3
* Change storages function calls
* env typo
* :pushpin: Automatic update of dependency thoth-common from 0.10.11 to 0.10.12
* :pushpin: Automatic update of dependency thoth-storages from 0.22.3 to 0.22.5
* schedule kebechet run
* Update doc and address coala issues
* Adjust name
* consumer template
* Remove unused debug env var
* Consumer metrics
* Add empty env template
* :pushpin: Automatic update of dependency thoth-common from 0.10.9 to 0.10.11
* Add metrics
* Handle hash disappearing
* Consumer deployment template
* Add doc strings
* import OpenShift. No major errors
* change decorator name
* Move message processing so we can add metrics to the functions
* Patch set comprehension
* Add metrics to consumer
* Remove metrics, it makes more sense to have them on the consumer side
* use thoth-logging and update hash-mismatch message
* Include which hashes are missing in hash mismatch
* Add thoth-sourcemanagement
* :pushpin: Automatic update of dependency thoth-storages from 0.21.11 to 0.22.3
* Work in progress commit for update consumer
* Update templates to reflect change in how script is run
* Use tuple as an item in hash
* add app for s2i
* Move app.py to package_update.py
* async calls
* Use app.sh to run faust app
* Convert app to faust app
* Use unique flag as to not check repeat packages
* remove limits on number of python-packages
* update topic names to thoth.package-update.X
* Update .thoth.yaml
* remove version metric
* relock
* Remove kafka imports
* Add openshift namespace for build trigger
* update templates for test-core
* Do not initialize/update database schema
* Install prometheus-client and minor changes from testing
* Add metrics to package-update-job
* README
* Styling
* mount ca.crt certificate
* create openshift templates and convert to faust
* Successfully posts to Kafka topics
* Initial commit
* use target-version and follow the convention
* :sparkels: a new template for PR
* use test env by default
* Update .thoth.yaml
* :green_heart: fixed the changelog
* :sparkles: added some more information
* :sparkles: added thoth config for stage environment
* :sparkles: added all the default project configs

## Release 0.8.0 (2020-08-25T15:42:00)
* :pushpin: Automatic update of dependency pytest from 6.0.0rc1 to 6.0.1 (#121)
* :pushpin: Automatic update of dependency pytest from 6.0.0rc1 to 6.0.1 (#118)
* :pushpin: Automatic update of dependency thoth-messaging from 0.5.0 to 0.6.7 (#120)
* :pushpin: Automatic update of dependency pylint from 2.5.3 to 2.6.0 (#119)
* :pushpin: Automatic update of dependency thoth-messaging from 0.5.0 to 0.6.7 (#115)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.5 to 0.25.5 (#114)
* :pushpin: Automatic update of dependency pylint from 2.5.3 to 2.6.0 (#117)
* :pushpin: Automatic update of dependency pre-commit from 2.6.0 to 2.7.1 (#116)
* :pushpin: Automatic update of dependency thoth-python from 0.10.0 to 0.10.1 (#113)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.0rc1 (#111)
* Feature/persistent metrics (#109)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.4 to 0.24.5 (#110)
* :pushpin: Automatic update of dependency thoth-messaging from 0.3.7 to 0.5.0 (#108)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.3 to 0.24.4 (#106)
* Remove latest versions limitation (#105)
* Remove unused env variable (#104)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.0rc1 (#103)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.0rc1 (#102)
* :pushpin: Automatic update of dependency thoth-messaging from 0.3.6 to 0.3.7 (#101)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.0rc1 (#100)
* :pushpin: Automatic update of dependency thoth-messaging from 0.3.6 to 0.3.7 (#99)
* :pushpin: Automatic update of dependency thoth-storages from 0.24.2 to 0.24.3 (#98)
* use asyncio for sending messages (#97)
* Remove templates handled by thoth-application (#96)
* Remove old bits (#95)
* enable pre-commit support for the application (#94)

## Release 0.8.1 (2020-09-07T22:57:53)
### Features
* update messaging and add component_name and version (#124)

## Release 0.8.2 (2020-09-25T07:49:35)
### Features
* remove consumer logic (moved to investigator) (#130)
* :truck: include aicoe-ci configuration file
### Automatic Updates
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#138)
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#137)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.0 to 0.7.6 (#136)
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#135)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.0 to 0.7.6 (#134)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.0 to 0.7.6 (#133)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.0 to 0.3.2 (#132)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.6 to 0.25.11 (#131)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.5 to 0.25.6 (#129)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.5 to 0.25.6 (#128)

## Release 0.8.3 (2020-10-02T15:15:21)
### Bug Fixes
* exception won't cause runtime failure (#151)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.8 to 0.7.10 (#160)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.8 to 0.7.10 (#159)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.13 to 0.25.14 (#158)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.12 to 0.25.13 (#157)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.7 to 0.7.8 (#156)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.11 to 0.25.12 (#155)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.0 (#154)
* :pushpin: Automatic update of dependency thoth-messaging from 0.7.6 to 0.7.7 (#153)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#144)
* :pushpin: Automatic update of dependency thoth-python from 0.10.1 to 0.10.2 (#143)

## Release 0.8.4 (2020-11-10T20:29:04)
### Features
* lock down thoth-messaging (#164)
### Automatic Updates
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#173)
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#172)
* :pushpin: Automatic update of dependency pre-commit from 2.7.1 to 2.8.2 (#171)
* :pushpin: Automatic update of dependency pre-commit from 2.7.1 to 2.8.2 (#170)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.2 to 0.3.3 (#169)
* :pushpin: Automatic update of dependency thoth-sourcemanagement from 0.3.2 to 0.3.3 (#168)
* :pushpin: Automatic update of dependency thoth-storages from 0.25.15 to 0.26.0 (#167)

## Release 0.8.5 (2021-02-08T19:05:59)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#189)
* :arrow_up: Automatic update of dependencies by Kebechet (#188)
* Messaging v0.8 (#185)
* :arrow_up: Automatic update of dependencies by kebechet. (#184)
* :arrow_up: autoupdate of pre-commit plugins
* :arrow_up: Automatic update of dependencies by kebechet. (#183)
* update .aicoe-ci.yaml (#178)
* :arrow_up: Automatic update of dependencies by kebechet. (#180)
* set base to v0.20.1 (#179)
* update .thoth.yaml (#177)
* port to python 38 (#176)
### Improvements
* removed bissenbay, thanks for your contributions!

## Release 0.8.6 (2021-02-08T20:42:56)
### Bug Fixes
* :four_leaf_clover: fix the typing extension installation issue (#192)

## Release 0.8.7 (2021-02-09T07:46:39)
### Improvements
* Removed unused package imports (#198)

## Release 0.8.8 (2021-06-03T17:36:19)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* flush all pending messages (#206)
* constrain thoth-messaging
* :arrow_up: Automatic update of dependencies by Kebechet (#203)
### Improvements
* :robot: ci updates w.r.t prow, thoth and aicoe-ci (#205)
* use py38 image
### Other
* remove thoth-sourcemanagement from dependencies (#207)

## Release 0.8.9 (2021-06-14T15:01:01)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.8.10 (2021-06-30T01:23:43)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* :zap: update to pydantic calling convention for messaging
* :arrow_up: Automatic update of dependencies by Kebechet

## Release 0.8.11 (2021-07-30T10:24:59)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet
