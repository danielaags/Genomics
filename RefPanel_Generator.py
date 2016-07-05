# Written by Daniela Garcia-Soriano, June 2016
# Python and shell script that automatically generates Reference Panels

import sys
import subprocess
import os
import random
import resource
import pandas as pd

"""
###When no filtered haplotipes files is provided:
### python RefPanel_Generator_v3.py ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes_260.vcf integrated_call_samples_v3.20130502.ALL.panel 
chr1 2 10 GBR GIH

###When filtered haplotipes files is provided:
### python RefPanel_Generator__.py ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes_260.vcf 
ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes_filtered.txt integrated_call_samples_v3.20130502.ALL.panel chr1 2 10 GBR GIH
"""

###Checking inputs###
if len(sys.argv) < 8:
	sys.stderr.write("Usage when no haplotipe_filtered file is provided: python REFpanel_master.py 0 haplotipes_file populations_file identifier_outputs number_ancenstral_populations number_max_individuals_to_take ancestral_population_1 ... ancestral_population_N ")
	sys.stderr.write("\n\nUsage when haplotipe_filtered file is provided: python REFpanel_master.py 1 haplotipes_file haplotipes_file_filtered populations_file identifier_outputs number_ancenstral_populations number_max_individuals_to_take ancestral_population_1 ... ancestral_population_N ")
	sys.exit("\n\nNot enough arguments given!!!")

#Getting all the inputs when no filter file is provided
if int(sys.argv[1]) == 0:

	#Haplotypes file
	hapfile = sys.argv[2]
	outhapfile = "filtered_" + hapfile

	#Ancestral populations
	#File with ancestral population
	ancpop = sys.argv[3]

	#Identifier outputs
	id = sys.argv[4]

	#Number of ancestral populations to get
	n = int(sys.argv[5])
	#Number of individious 
	stop = int(sys.argv[6])

	#Filter to eliminate values non-identify by RFMix by picking the ones identify by RFMix
	command = " grep '0|0\|0|1\|1|0\|1|1' " + hapfile + ">" +  outhapfile
	subprocess.call (command, shell=True)

	#awk entries to start and end
	#Start will be designed as zero
	sta_hap = str(1)

	#Get the end of the file
	command = "wc -l " + outhapfile + " | cut -d " + outhapfile[0] + " -f1 | sed s/\ //g"
	end_hap = subprocess.check_output(command, shell = True)
	end_hap = end_hap.rstrip()
	print(end_hap)
	#Change the value of the last row in the file
	#end_hap = end_hap[0]

	#Keeps track of the number of individuos to extract after being randomly selected
	num = [None] * n
	#print(num)
	
	extra = 7

#Getting all the inputs when no filter file is provided
if int(sys.argv[1]) == 1:

	#Haplotypes file
	#hapfile = sys.argv[2]
	outhapfile = sys.argv[2]

	#Ancestral populations
	#File with ancestral population
	ancpop = sys.argv[3]

	#Identifier outputs
	id = sys.argv[4]

	#Number of ancestral populations to get
	n = int(sys.argv[5])
	#Number of individious 
	stop = int(sys.argv[6])

	#Filter to eliminate values non-identify by RFMix by picking the ones identify by RFMix
	#command = " grep '0|0\|0|1\|1|0\|1|1' " + hapfile + ">" +  outhapfile
	#subprocess.call (command, shell=True)

	#awk entries to start and end
	#Start will be designed as zero
	sta_hap = str(1)

	#Get the end of the file
	command = "wc -l " + outhapfile + " | cut -d " + outhapfile[0] + " -f1 | sed s/\ //g"
	end_hap = subprocess.check_output(command, shell = True)
	end_hap = end_hap.rstrip()
	print(end_hap)

	#Keeps track of the number of individuos to extract after being randomly selected
	num = [None] * n
	#print(num)
	
	extra = 8

	
###Get the physical position and alleles from the chromosome under analysis###
pos_chr_legend = id +  "_reference_legend.txt"
#awk 'NR>=254&&NR<=6468347{print}NR>=6468347{exit}' ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes_filtered.vcf  | awk '{ print $3 " " $2 " " $4 " " $5}' | tr '\t' ' ' > chr1.reference_4col.legend &
command = "awk 'NR>=" + sta_hap + "&&NR<=" + end_hap + "{print}NR>=" + end_hap + "{exit}' " + outhapfile + " | awk '{ print $3 \" \" $2 \" \" $4 \" \" $5}' | tr '\\t' ' ' > " + pos_chr_legend
print (command)
subprocess.call (command, shell=True)
print("Physical position and alleles have been saved\n")

ref_pan = id + "_full_reference_panel.txt"

#Ancentral population will be given in argument 5 onwards
for i in range(n):
	indx = i + extra
	pop = sys.argv[indx]
	
	#Take random number of invidious
	num[i]=random.randrange(1,stop)
	#print (num)
	
	#Extract $num position from pop_i
	outpop = str(num[i]) + "_" + pop + "_positions.txt" 
	command = "grep -n " + pop + " " + ancpop + " | cut -d ':' -f1 | head -n " +  str(num[i]) + " > "  + outpop
	subprocess.call (command, shell=True)
	
	###Get the ranges pop_i###
	command = "awk 'NR==1{first=$1;last=$1;next} $1 == last+1 {last=$1;next} {print first,last;first=$1;last=first} END{print first,last}' " +  outpop + " > pop_ranges.txt"
	subprocess.call (command, shell=True)
	
	#Turn data into a .csv file
	command = "cat pop_ranges.txt | tr ' ' ',' > pop_ranges.csv "
	subprocess.call (command, shell=True)
	#Read the ranges using pandas
	r = pd.read_csv("./pop_ranges.csv", header = None)
	#Get the number of rows
	m = len(r.index)

	#print(m)

	#For to save the ranges and extract the selected haplotypes
	for j in range(m):
		#Name of the file
		outpop_rescued = str(num[i]) + "_" + pop + "_rescued_cut.txt" 
		#Cut may do the same as awk
		command = "cut -f" + str(r.iloc[j,0]+8) + "-" + str(r.iloc[j,1]+8) + " " + outhapfile + " |  tr '|' ' ' | tr '\\t' ' '  > " + outpop_rescued
		subprocess.call (command, shell=True)
		#If ranges are given in more than one line
		if j > 0:
			#Temporal file to save ranges, if needed
			command = "cut -f" + r.iloc[j,0] + "-" + r.iloc[j,1] + " " + outhapfile + " |  tr '|' ' ' | tr '\\t' ' '  >  temporal_rescued_cut.txt"
			subprocess.call (command, shell=True)
			#The paste command allows the column concatenation needed in this case
			command = "paste -d ' ' " + outpop_rescued + " temporal_rescued_cut.txt > tmp.txt"	
			subprocess.call (command, shell=True)
			command = "mv tmp.txt "  + outpop_rescued
			subprocess.call (command, shell=True)
	
	outpop_rescued = str(num[i]) + "_" + pop + "_rescued_cut.txt"
	
	if i == 0:
		#paste -d " " chr1.reference_4col.legend 40_CHB_rescued_cut.txt 40_YRI_rescued_cut.txt > 40_full_raw_dataset_4col_CHB_YRI.txt &
		command = "paste -d ' ' " + pos_chr_legend + " " + outpop_rescued + " > " + ref_pan
		subprocess.call (command, shell=True)
		#command = "cat " + ref_pan 
		#subprocess.call (command, shell=True)
	else:
		#A >> generates a file with more rows than the ones rescued. By substituting the file, the number of rows are preserved.
		command = "paste -d ' ' " + ref_pan + " " + outpop_rescued + " > tmp.txt" 
		subprocess.call (command, shell=True)
		command = "mv tmp.txt " + ref_pan
		subprocess.call (command, shell=True)
		#command = "cat " + ref_pan 
		#subprocess.call (command, shell=True)
			
			
print("Ancenstral populations have beed rescued\n and Reference Panel was generated\n")
	
###Remove temporal files###
command = "rm -f -r pop_ranges.txt"
subprocess.call(command, shell=True)
command = "rm -f -r pop_ranges.csv"
subprocess.call(command, shell=True)
command = "rm -f -r temporal_rescued_cut.txt"
subprocess.call(command, shell=True)

###Generate a new folder to save the files created, move .txt files and report them###
out_folder = id + "_" + "output"
os.mkdir(out_folder)
command = "mv *txt " + out_folder
subprocess.call(command, shell=True)
print("Files generated and moved to " + out_folder)
command = "ls " +  out_folder + "| grep '.txt' "
print(subprocess.check_output(command, shell=True))	

mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print "memory usage:", mem
