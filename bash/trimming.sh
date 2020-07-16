#!/bin/bash
#Trimming step. One has to provide the raw reads names in a .txt file.

reads=$1

#Read each line
cat $reads | while read line1; read line2
do
	#echo "$line1" "$line2"
	name=`echo "$line1" | cut -d '_' -f1`
	AdapterRemoval --file1 "$line1" --file2 "$line2" --qualitybase 33 --basename "$name" --gzip --trimqualities --minquality 20 --minlength 20
done