Thoth Package  Update Job
--------------------------

.. image:: https://img.shields.io/github/v/tag/thoth-station/package-update-job?style=plastic
  :target: https://github.com/thoth-station/package-update-job/tags
  :alt: GitHub tag (latest by date)

.. image:: https://quay.io/repository/thoth-station/package-update-job/status
  :target: https://quay.io/repository/thoth-station/package-update-job?tab=tags
  :alt: Quay - Build

This job iterates over the packages in our database to ensure that they:

* still exist
* haven't changed

This job is run periodically as an OpenShift CronJob. The job checks the availability
of packages as well as their hashes to make sure they match what Thoth has stored.

Logic behind package update
============================================

We get a list of all packages which we have analyzed. Then, we check whether.

* the package still exists on that index
* that version of the package still exists
* if the SHA256 from source matches what we have stored

If we find any of these issues we post to a Kafka topic so that a consumer can
decide how to handle the update.

Installation and Deployment
===========================

The job is an OpenShift s2i build, the deployment is done via Kustomize,
deployment templates are live in the `core repository <https://github.com/thoth-station/thoth-application/tree/master/package-update/overlays/test>`__.

Running the job locally
=======================

You can run this job locally without a cluster deployment. To do so, prepare
your virtual environment:

.. code-block:: console

  $ pipenv install  --dev # Install all the requirements

After that, you need to run a local instance of database - follow
`instructions in the README <https://github.com/thoth-station/storages#running-postgresql-locally>`__ file for
more info and prepare the database schema:

  $ pipenv run python3 ./app.py

Job will talk to your local database instance by default which is located at
```localhost:5432`` by default. And your local Kafka instance which is ``localhost:9092``
by default.
