#!/bin/bash

git log --format="%ae" | sort | uniq | wc -l | awk '{print "Number of authors: "$1}'
git log --format="%ar;/%an <%ae>" --since="1 year ago" | awk -F ";" '{print $2}' | sort | uniq -c | awk -F "/" 'max==""||$1>max {max=$1;value=$2} END {print "Most active author within last year: "value}'
git log --format="%ct-%cr" | tail -n 1 | awk -F "-" -v date="$(date +%s)" '{printf "Time range of development: %.0f days (started " $2")\n", ((date - $1) / (24 * 3600))}'
git log --max-parents=1 --format="%s"| grep -E "fix|rewrite|doc|test|improve" | wc -l | awk -v total=$(git log --max-parents=1 --format="%s" | wc -l) '{printf "Share of maintenance: %.1f%\n", $1 / total * 100}'
git log --max-parents=1 --format="" --since="1 year ago" --name-only | sort | uniq | wc -l | awk -v total=$(find . -type f | wc -l) '{printf "Share of stale code: %.1f%\n", (1-($1/total)) * 100}'
 git log --format="%s" --since="1 month ago" | tr " " "\n" | tr '[:upper:]' '[:lower:]' | grep -ivwE "a|an|at|for|from|in|is|of|on|the|to|use|with|when|[^#\w]" | sort | uniq -c | sort -ri | head -n 10 | awk '{print $2}' | tr "\n" " " | join_by , | awk '{print "Top 10 commit message keywords last month: "$1}'
