#!/usr/bin/env sh
#
# This script is run by OpenShift's s2i. Here we guarantee that we run desired
# command
#

if [ "$SUBCOMMAND" = "producer" ]
then
    if [ "$FAUST_DEBUG" != "0" && "$FAUST_DEBUG" != "" ]
    then
        exec pipenv run faust --debug --loglevel debug -A producer main
    else
        exec pipenv run faust -A producer main
    fi
elif [ "$SUBCOMMAND" = "consumer" ]
then
    if [ "$FAUST_DEBUG" != "0" && "$FAUST_DEBUG" != "" ]
    then
        exec pipenv run faust --debug --loglevel debug -A consumer worker
    else
        exec pipenv run faust -A consumer worker
    fi
fi
