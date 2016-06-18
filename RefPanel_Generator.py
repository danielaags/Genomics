# Written by Daniela Garcia-Soriano, June 2016
# Python and shell script that automatically generates Reference Panels

import sys
import subprocess
import os

### python REFpanel_master.py ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes_260.vcf integrated_call_samples_v3.20130502.ALL.panel chr1 254 259 2 20 GBR GIH
###Checking inputs###
if len(sys.argv) < 6:
	sys.stderr.write("Usage: python REFpanel_master.py haplotipes_file populations_file identifier_outputs start_line_haplotipes_file end_line_haplotipes_file number_ancenstral_populations number_individuals_to_take ancestral_population_1 ... ancestral_population_N ")
	sys.exit("\n\nNot enough arguments given!!!")

#Getting all the inputs

#Haplotypes file
hapfile = sys.argv[1]
outhapfile = hapfile[:-4] + "_filtered.txt"

#Ancestral populations
#File with ancestral population
ancpop = sys.argv[2]

#Line to start haplotype filtering
sta_hap = sys.argv[4]
#Line to finish haplotype filtering
end_hap = sys.argv[5]

#Identifier outputs
id = sys.argv[3]

#Number of ancestral populations to get
n = int(sys.argv[6])
#Number of individious 
num = sys.argv[7]

#Filter to eliminate values non-identify by RFMix
command = " grep '0|0\|0|1\|1|0\|1|1' " + hapfile + ">" +  outhapfile
subprocess.call (command, shell=True)

#awk entries to start and end
#Start will be designed as zero
sta_hap = str(1)

#Get the end of the file
command = "wc -l " + outhapfile + " | cut -d " + hapfile[0] + " -f1 | sed s/\ //g "
end_hap = subprocess.check_output(command, shell = True)
#print("Before filtering: " + end_hap + "\nAfter filtering: "+ endouthapfile)
#Change the value of the last row in the file
end_hap = end_hap[:-1]

#Number of individuos to extract
num = [None] * n
#print(num)

#Ancentral population will be given in argument 5 onwards
for i in range(n):
	indx = i + 6
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
	
	#Get the number of output lines
	command = "wc -l pop_ranges.txt"
	m = subprocess.check_output (command, shell=True)
	m = int(m[0])
	#print(m)

	#For to save the ranges and extract the selected haplotypes
	for j in range(m):
		#Where to start
		command = "sed -n " + str(j+1) + "p pop_ranges.txt | cut -d ' ' -f1 | sed s/\ //g "
		s = subprocess.check_output (command, shell=True)
		# First haplotype starts in column 8
		s = int(s[:-1]) + 8
		#Where to end
		command = "sed -n " + str(j+1) + "p pop_ranges.txt | cut -d ' ' -f2 | sed s/\ //g "
		e = subprocess.check_output (command, shell=True)
		e = int(e[:-1]) + 8
		#Get the data
		outpop_rescued = str(num[i]) + "_" + pop + "_rescued_cut.txt" 
		#Cut may do the same as awk
		command = "cut -f" + str(s) + "-" + str(e) + " " + outhapfile + " |  tr '|' ' ' | tr '\\t' ' '  > " + outpop_rescued
		subprocess.call (command, shell=True)
		#If ranges are given in more than one line
		if j > 0:
			#Temporal file to save ranges, if needed
			command = "cut -f" + str(s) + "-" + str(e) + " " + outhapfile +  " |  tr '|' ' ' | tr '\\t' ' '  >  temporal_rescued_cut.txt"
			subprocess.call (command, shell=True)
			#The paste command allows the column concatenation needed in this case
			command = "paste -d ' ' " + outpop_rescued + " temporal_rescued_cut.txt > tmp.txt"	
			subprocess.call (command, shell=True)
			command = "mv tmp.txt "  + outpop_rescued
			subprocess.call (command, shell=True)
			
			
print("Ancenstral populations have beed rescued\n")

###Get the physical position and alleles from the chromosome under analysis###
pos_chr_legend = id +  "_reference_legend.txt"
command = "awk 'NR>=" + sta_hap + "&&NR<=" + end_hap + "{print}NR>=" + end_hap + "{exit}' " + outhapfile + " | awk '{ print $3 \" \" $2 \" \" $4 \" \" $5}' | tr '\\t' ' ' > " + pos_chr_legend
subprocess.call (command, shell=True)
print("Physical position and alleles have been saved\n")


###Generate de reference panel###
ref_pan = id + "_full_reference_panel.txt"
for i in range(n):
	indx = i + 6
	pop = sys.argv[indx]
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
		
print("Reference Panel Generated\n")	

###Remove temporal files###
command = "rm -f -r pop_ranges.txt"
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
