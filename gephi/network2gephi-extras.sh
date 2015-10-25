#!/usr/bin/env bash
echo "Source\tTarget\tLabel"
#awk -F\" '{print "\"" $8 "\", \"" $(10) "\", \"" $(12) "\", \"" $(14) " / " $16 "\""}' $1
awk -F\" '{print "\"" $8 "\"\t \"" $(10) "\"\t \"" $(12) " with " $(14) " / " $16 "\""}' $1
