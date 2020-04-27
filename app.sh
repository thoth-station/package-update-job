#!/usr/bin/env sh
#
# This script is run by OpenShift's s2i. Here we guarantee that we run desired
# command
#

if [ "$SUBCOMMAND" = "producer" ]
then
    if [ "$FAUST_DEBUG" != "0" && "$FAUST_DEBUG" != "" ]
    then
        exec faust --debug --loglevel debug -A package_update main
    else
        exec faust -A package_update main
    fi
elif [ "$SUBCOMMAND" = "consumer" ]
then
    if [ "$FAUST_DEBUG" != "0" && "$FAUST_DEBUG" != "" ]
    then
        exec faust --debug --loglevel debug -A update_consumer worker
    else
        exec faust -A update_consumer worker
    fi
fi
