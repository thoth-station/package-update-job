# Changelog for Thoth's Template GitHub Project

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
