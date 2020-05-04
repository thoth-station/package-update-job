#!/usr/bin/env sh
#
# This script is run by OpenShift's s2i. Here we guarantee that we run desired
# command
#

if [ "$SUBCOMMAND" = "producer" ]
then
    if [ "$FAUST_DEBUG" != "0" && "$FAUST_DEBUG" != "" ]
    then
        exec pipenv run faust --debug --loglevel debug -A package_update.package_update main
    else
        exec pipenv run faust -A package_update.package_update main
    fi
elif [ "$SUBCOMMAND" = "consumer" ]
then
    if [ "$FAUST_DEBUG" != "0" && "$FAUST_DEBUG" != "" ]
    then
        exec pipenv run faust --debug --loglevel debug -A package_update.update_consumer worker
    else
        exec pipenv run faust -A package_update.update_consumer worker
    fi
fi
