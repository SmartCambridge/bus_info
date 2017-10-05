#!/bin/bash

# Find services that don't have exactly one OperatingProfile

for f in *.xml
do
    n=$(xmlstarlet sel -t -v 'count(/_:TransXChange/_:Services/_:Service/_:OperatingProfile)' ${f})
    if [ "${n}" != "1" ]
    then
	echo "Problem with ${f}"
    fi
done
