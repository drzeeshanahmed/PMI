# Input: CSV of gene expression file, i.e. annotated RNA sequencing results with
# columns for gene ID and some measure of abundance (preferably TPM)

# Output: CSV of all gene IDs from input file sorted by TPM in descending order
# Columns: sample_id, gene_id, TPM 

# How to use this script:
# $ python scriptname.py geneExpfile Output_Directory

import csv
import sys
import itertools

def main():
    filepath = sys.argv[1] # the full path to the sample file
    filesplit = filepath.split('/')
    filename = filesplit[-1]

    # Import and collect relevant data into a dictionary
    with open(filepath) as currentFile:
        myreader = csv.reader(currentFile, delimiter = '\t')
        tpmDict = {} # Will hold gene_id (keys) and TPM (values) in a dictionary
        for line in myreader:
            if line[0] == 'gene_id':
                # don't include header in dictionary
                pass
            else:
                tpmDict.update({line[0]:float(line[-2])})

    # Sort by descending TPM (values)
    sortedTPM = sorted(tpmDict.items(), key = lambda pair: pair[1] ,reverse = True)

    # Output into another text file
    outFileName = filename + "_sorted_genes_all"
    outPath = sys.argv[2] +"/" + outFileName
    with open(outPath, 'w') as newfile:
        highestGenesWriter = csv.writer(newfile, delimiter = ',')
        # Create header row
        highestGenesWriter.writerow(['sample_id', 'gene_id', 'TPM']) # a row is a list

        # Loop through the new dictionary using sortedTPM and write
        # all this information into the new file.
        #for gene in itertools.islice(sortedTPM, 20): # use for top 20 only
        for gene in sortedTPM:
            gene_id = gene[0]
            expression = gene[1]
            highestGenesWriter.writerow([str(filename), gene_id, expression])


if __name__ == '__main__':
    main()
