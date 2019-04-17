git log --format="%ae" | sort | uniq | wc -l | awk '{print "Number of authors: "$1}'
git log --format="%ar;/%an <%ae>" --since="1 year ago" | awk -F ";" '{print $2}' | sort | uniq -c | awk -F "/" 'max==""||$1>max {max=$1;value=$2} END {print "Most active author within last year: "value}'
git log --format="%ar" | tail -n 1 | awk '{print "Time range of development: " $0}'

