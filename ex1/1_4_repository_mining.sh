#!/bin/bash

git log --format="%ae" | sort | uniq | wc -l | awk '{print "Number of authors: "$1}'
git log --format="%ar;/%an <%ae>" --since="1 year ago" | awk -F ";" '{print $2}' | sort | uniq -c | awk -F "/" 'max==""||$1>max {max=$1;value=$2} END {print "Most active author within last year: "value}'
git log --format="%ct-%cr" | tail -n 1 | awk -F "-" -v date="$(date +%s)" '{printf "Time range of development: %.0f days (started " $2")\n", ((date - $1) / (24 * 3600))}'
git log --max-parents=1 --format="%s"| grep -E "fix|rewrite|doc|test|improve" | wc -l | awk -v total=$(git log --max-parents=1 --format="%s" | wc -l) '{printf "Share of maintenance: %.1f%\n", $1 / total * 100}'

