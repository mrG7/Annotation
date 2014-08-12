import sys,re,fileinput,os

Argument = []
Argument = sys.argv[1:] 

if (len(Argument)) < 3:
        print "Usage: Input_variant Biomart_anotation Output_file" 
        sys.exit()

Filepath_variant = Argument[0]
Filepath_annotation = Argument[1]
output_path = Argument[2]

Gene_info = {}
Gene_loc = {}

Transcript_info = {}
Transcript_loc = {}

Exon_info = {}
Exon_loc = {}

GT = {}
TE = {}
Tnumberexons = {}

for line in fileinput.input([Filepath_annotation]):
	if line.startswith("Ensembl"):
		continue

        rowlist = []
        rowlist = (line.rstrip("\n")).split('\t')

	if rowlist[10] != "protein_coding":
		continue

	Gene_info[rowlist[0]] = ""
	Gene_info[rowlist[0]] = rowlist[8]+"\t"+str(" ".join(rowlist[9].split()))+"\t"+rowlist[2]+"\t"+rowlist[3]+"\t"+rowlist[4]

	Transcript_info[rowlist[1]] = ""
	Transcript_info[rowlist[1]] = rowlist[8]+"\t"+str(" ".join(rowlist[9].split()))+"\t"+rowlist[2]+"\t"+rowlist[5]+"\t"+rowlist[6]

	Exon_info[rowlist[-1]] = ""
	Exon_info[rowlist[-1]] = rowlist[8]+"\t"+str(" ".join(rowlist[9].split()))+"\t"+rowlist[-2]

	if rowlist[0] not in GT:
		GT[rowlist[0]] = []
		GT[rowlist[0]].append(rowlist[1])
	else:
		if rowlist[1] not in  GT[rowlist[0]]:
			GT[rowlist[0]].append(rowlist[1])

	if rowlist[1] not in TE:
                TE[rowlist[1]] = []
                TE[rowlist[1]].append(rowlist[-1])
        else:
                TE[rowlist[1]].append(rowlist[-1])
	
	if rowlist[2] not in Gene_loc:
		Gene_loc[rowlist[2]] = {}
		if rowlist[0] not in Gene_loc[rowlist[2]]:
			Gene_loc[rowlist[2]][rowlist[0]] = []
			Gene_loc[rowlist[2]][rowlist[0]].append(int(rowlist[3]))
			Gene_loc[rowlist[2]][rowlist[0]].append(int(rowlist[4]))
	else:
		if rowlist[0] not in Gene_loc[rowlist[2]]:
                        Gene_loc[rowlist[2]][rowlist[0]] = []
                        Gene_loc[rowlist[2]][rowlist[0]].append(int(rowlist[3]))
                        Gene_loc[rowlist[2]][rowlist[0]].append(int(rowlist[4]))

 
	if rowlist[2] not in Transcript_loc:
                Transcript_loc[rowlist[2]] = {}
                if rowlist[1] not in Transcript_loc[rowlist[2]]:
			Transcript_loc[rowlist[2]][rowlist[1]] = []
                        Transcript_loc[rowlist[2]][rowlist[1]].append(int(rowlist[5]))
			Transcript_loc[rowlist[2]][rowlist[1]].append(int(rowlist[6]))

	else:
		if rowlist[1] not in Transcript_loc[rowlist[2]]:
                        Transcript_loc[rowlist[2]][rowlist[1]] = []
                        Transcript_loc[rowlist[2]][rowlist[1]].append(int(rowlist[5]))
                        Transcript_loc[rowlist[2]][rowlist[1]].append(int(rowlist[6]))

	if rowlist[2] not in Exon_loc:
                Exon_loc[rowlist[2]] = {}
                if rowlist[-1] not in Exon_loc[rowlist[2]]:

                        Exon_loc[rowlist[2]][rowlist[-1]] = []
			Exon_loc[rowlist[2]][rowlist[-1]].append(int(rowlist[-4]))
			Exon_loc[rowlist[2]][rowlist[-1]].append(int(rowlist[-3]))

	else:
		if rowlist[-1] not in Exon_loc[rowlist[2]]:
                        Exon_loc[rowlist[2]][rowlist[-1]] = []
                        Exon_loc[rowlist[2]][rowlist[-1]].append(int(rowlist[-4]))
                        Exon_loc[rowlist[2]][rowlist[-1]].append(int(rowlist[-3]))


print len(Gene_loc.keys()),len(Gene_info.keys())
print len(Transcript_loc.keys()),len(Transcript_info.keys())

def span_gene_features(chr_v, start_v, end_v, eff_v):

	chr = ""
	start = 0
	end = 0
	effect = ""

	chr = str(chr_v)
	start = int(start_v)
	end = int(end_v)
	effect = str(eff_v)
	
	status = ""
	
	if end-start >= 10000:
		status = str(end-start)+"\tHIGH"
	elif  end-start >= 2000 and end-start < 10000:
		status = str(end-start)+"\tMEDIUM"
	else:
		status = str(end-start)+"\tLOW"


	output.write(str(status)+"\t")
	
	#print GT["ENSMUSG00000051951"]
	
	for gene in Gene_loc[chr]:
		if Gene_loc[chr][gene][0] >= start-500 and Gene_loc[chr][gene][1] <= end+500:

			output.write(str(gene)+",WHOLE_GENE("+str(Gene_info[gene])+"); ")
			output_level.write(str(gene)+"\t"+str(chr)+"\t"+str(start)+"\t"+str(end)+"\t"+str(effect)+"\t"+str(status)+"\tWHOLE_GENE\t\t\t"+str("\t".join(Gene_info[gene].split("\t")))+"\n")
			continue

		if end < Gene_loc[chr][gene][0] or start >  Gene_loc[chr][gene][1]:
			continue
	
		for transcript in GT[gene]:

			if end < Transcript_loc[chr][transcript][0] or start >  Transcript_loc[chr][transcript][1]:
                        	continue
	
			output.write(str(transcript)+",Total_Exons: "+str(len(TE[transcript]))+",")	

			if Transcript_loc[chr][transcript][0] >= start-200 and Transcript_loc[chr][transcript][1] <= end+200:
        			output.write("WHOLE_TRANSCRIPT,("+str(Transcript_info[transcript])+"); ")
				output_level.write(str(transcript)+"\t"+str(chr)+"\t"+str(start)+"\t"+str(end)+"\t"+str(effect)+"\t"+str(status)+"\tWHOLE_TRANSCRIPT\t\t\t"+str("\t".join(Transcript_info[transcript].split("\t")))+"\n")

			if Transcript_loc[chr][transcript][0] <= start and Transcript_loc[chr][transcript][1] >=  end:
				Flag = "False"
				count = 0
				for exon in TE[transcript]:
					if Exon_loc[chr][exon][0] >= start-100 and Exon_loc[chr][exon][1] <= end+100:
						Flag = "True"
						count = count + 1
                        			output.write(str(exon)+","+str(Exon_info[exon])+": ")

				if Flag == "False":
					output.write("INTRONIC,("+str(Transcript_info[transcript])+"); ")
				else:
					output_level.write(str(transcript)+"\t"+str(chr)+"\t"+str(start)+"\t"+str(end)+"\t"+str(effect)+"\t"+str(status)+"\tPARTIAL_TRANSCRIPT\t"+str(len(TE[transcript]))+"\t"+str(round(float(count)/float(len(TE[transcript])),2))+"\t"+str("\t".join(Transcript_info[transcript].split("\t")))+"\n")

                	if Transcript_loc[chr][transcript][0] <= start and Transcript_loc[chr][transcript][1] <=  end and Transcript_loc[chr][transcript][1] > start:
   				Flag = "False"
				count = 0
	                     	for exon in TE[transcript]:
                                        if Exon_loc[chr][exon][0] >= start-100 and Exon_loc[chr][exon][1] <= end+100:
						Flag = "True"
						count = count+1
                                        	output.write(str(exon)+","+str(Exon_info[exon])+": ")

				if Flag == "False":
                                	output.write("INTRONIC,("+str(Transcript_info[transcript])+"); ")

				else:
                                        output_level.write(str(transcript)+"\t"+str(chr)+"\t"+str(start)+"\t"+str(end)+"\t"+str(effect)+"\t"+str(status)+"\tPARTIAL_TRANSCRIPT\t"+str(len(TE[transcript]))+"\t"+str(round(float(count)/float(len(TE[transcript])),2))+str(count)+"\t"+str("\t".join(Transcript_info[transcript].split("\t")))+"\n")

				
                	if Transcript_loc[chr][transcript][0] >= start and Transcript_loc[chr][transcript][1] >=  end and Transcript_loc[chr][transcript][0] < end:
 				Flag = "False"
				count = 0
				for exon in TE[transcript]:
                                        if Exon_loc[chr][exon][0] >= start-100 and Exon_loc[chr][exon][1] <= end+100:
						Flag = "True"
						count = count + 1
                                        	output.write(str(exon)+","+str(Exon_info[exon])+": ")
				
				if Flag == "False":
                               		output.write("INTRONIC,("+str(Transcript_info[transcript])+"); ")
				else:
                                	output_level.write(str(transcript)+"\t"+str(chr)+"\t"+str(start)+"\t"+str(end)+"\t"+str(effect)+"\t"+str(status)+"\tPARTIAL_TRANSCRIPT\t"+str(len(TE[transcript]))+"\t"+str(round(float(count)/float(len(TE[transcript])),2))+"\t"+str("\t".join(Transcript_info[transcript].split("\t")))+"\n")
				           
	output.write("\n")


output = open(output_path,"w")
output_level = open(output_path+"_whole_gene_features","w")

for line1 in fileinput.input([Filepath_variant]):

	if line1.startswith("#"):
		continue

        rowlist1 = []
        rowlist1 = (line1.rstrip("\n")).split('\t')
	#print rowlist1


	
	begin = 0
	end = 0
	vtype = ""	

	begin = int(rowlist1[1])
	end = int(((rowlist1[7].split(";"))[0]).lstrip("END="))
	vtype = (((rowlist1[7].split(";"))[-2]).lstrip("END="))

	if int(end-begin) < 100:
		continue

	output.write(line1.rstrip("\n")+"\t")

	span_gene_features(rowlist1[0].lstrip("chr"), begin, end,vtype )

output.close()
output_level.close()
