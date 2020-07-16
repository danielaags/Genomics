#!/bin/bash
#The sript search for the organism name in either the GB or the refseq lists and gives back the link to download
list=$1
filename=$2
echo "assembly_acc bioproject organism link" > genLinks.txt
cat $list | while read line
do
    #reading each line
    #echo "Organism $line"
    #output=$(cat $filename | grep -E $line | cut -f 8,20)
    echo "$line"
    cat $filename | grep -E $line | cut -f 1,2,8,20 >> genLinks.txt
done
echo "Done"
