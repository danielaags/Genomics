#!/bin/bash
#The sript search for the organism name in either the GB or the refseq lists and gives back the link to download
list=$1
cat $list | while read line
do
    #reading each line
    echo "$line"
    mv $line* APD_cluster
done
echo "Done"