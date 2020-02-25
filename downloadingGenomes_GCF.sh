#!/bin/bash
list=$1
source=$2
bash ./findgenomes.sh $list $source
echo 'Done links'
#Split into two files, one as a reference and the other just with the links
cat genLinks.txt | cut -f 1,2,3 > referenceGenome.txt
cat genLinks.txt | cut -f 4 > linksGenomes.txt
echo 'Done sppliting'
#Make new scripts to download the data: i)sequence, ii)genomic annotation, iii)protein annotation
awk 'BEGIN{FS=OFS="/";filesuffix="genomic.fna.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print "wget "ftpdir,file}' linksGenomes.txt > download_fna_files.sh
awk 'BEGIN{FS=OFS="/";filesuffix="genomic.gff.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print "wget "ftpdir,file}' linksGenomes.txt > download_genomic_gff_files.sh
awk 'BEGIN{FS=OFS="/";filesuffix="protein.gpff.gz"}{ftpdir=$0;asm=$10;file=asm"_"filesuffix;print "wget "ftpdir,file}' linksGenomes.txt > download_protein_gpff_files.sh
echo 'Done sh'
#Download sequences
source download_fna_files.sh
mkdir genomic_fna
mv *gz* genomic_fna
echo 'Genomic ready'
#Download genomic accotations
source download_genomic_gff_files.sh
mkdir g_annotation_gff
mv *gz* g_annotation_gff
echo 'Genomic annotations ready'
#Download protein annotations
source download_protein_gpff_files.sh
mkdir p_annotation_gpff
mv *gz* p_annotation_gpff
echo 'Protein annotations ready'

