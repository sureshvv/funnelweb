grep '^--' $1 | awk '{print $3}' | grep -v '^(try:' | sed -e 's?http://[^/]*??' -e 's:/$::' | sort | uniq > $1.urls


