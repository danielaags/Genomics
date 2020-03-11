#!/bin/bash
#The sript search for the organism name in either the GB or the refseq lists and gives back the link to download
list=$1
filename=$2
echo "assembly_acc bioproject organism strain link" > genLinks.txt
cat $list | while read line
do
    #reading each line
    echo "$line"
    #echo "cat $filename | grep -w $line | cut -f1,2,8,20" 
    cat $filename | grep -F "$line" | cut -f1,2,8,20 >> genLinks.txt
done
echo "Done"
