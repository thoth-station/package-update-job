#!/usr/bin/env sh
#
# This script is run by OpenShift's s2i. Here we guarantee that we run desired
# command
#

if [ "$SUBCOMMAND" = "producer"]
    exec faust --debug --loglevel debug -A package_update main
fi
