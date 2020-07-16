#!/bin/bash
#Whole variant calling steps included

#bcftools need to be called every time
export PATH=/Users/danielaagarcia-soriano/bin/bcftools/:$PATH

#Input files
reads=$1
genome=$2

#Genome index
#bwa index $genome

#Read each line
cat $reads | while read line1; read line2
do
	#echo "$line1" "$line2"
	name=`echo "$line1" | cut -d '.' -f1`
	#alignment
	bwa mem -t2 $genome trimmed/$line1 trimmed/$line2 > $name.sam
	#into sam
	samtools sort -@2 -o $name.bam $name.sam
	samtools index $name.bam
	samtools mpileup -u -d 999 -L 999 -f $genome $name.bam > $name.bcf
	#variant calls
	bcftools call -c -v -Oz $name.bcf > $name.vcf.gz
	bcftools index $name.vcf.gz
	#information extraction
	gunzip $name.vcf.gz
	bcftools query -f '%POS %REF %ALT\n' $name.vcf > $name.txt

done