# This script compares a list of genes from File 1 (a source file) to a list of
# genes in File 2 (a reference file) and outputs a list of genes that are
# present in both files.

# The reference file should also include gene names and descriptions for each
# gene ID, since this information will be included in the output file.

# Output file columns: sample_id, gene_id, TPM, gene_name, gene_disease

# Use in command line:
# $ python scriptname.py path/to/sourcefile path/to/referencefile Output_Directory

# Currently only allows for use of one (1) reference file at a time.

import csv
import sys

def main():
    file1path = sys.argv[1] # the full path to the source file
    file1split = file1path.split('/')
    file1name = file1split[-1]

    file2path = sys.argv[2] # the full path to the reference file
    file2split = file2path.split('/')
    file2name = file2split[-1]

    # Import genes from File 2 (reference file) into a dictionary
    # with GD_Ensembl_Id (key) and GD_Gene_Name (value)
    with open(file2path) as refFile:
        myreader = csv.reader(refFile, delimiter = ',')
        geneList = {}
        geneDescriptions = {}

        for line in myreader:
            if line[0] == 'GD_Gene_Name':
                pass # skip the header line
            else:
                # 1st column is 'GD_Gene_name'
                # 2nd column is 'GD_Ensembl_Id'
                geneList.update({line[1]:line[0]})
                geneDescriptions.update({line[1]:line[4]})
    #print(geneList)
    #print(geneDescriptions)

    # Open File 2 (reference) and create an output file
    referenceType = file2name.split('_')[1]
    outFileName = file1name + '_' + referenceType + '_genes_only_nonzero'
    outPath = sys.argv[3] + "/" + outFileName
    with open(file1path) as sourcefile, open(outPath, 'w') as newfile:
        sourceReader = csv.reader(sourcefile, delimiter = ',')
        cardioGenesWriter = csv.writer(newfile, delimiter = ',')
        # Header line in output file:
        cardioGenesWriter.writerow(['sample_id', 'gene_id', 'TPM', 'gene_name','gene_disease'])

        # Go through each line in File 1 (source) and compare the gene ID
        # to the ones in File 2 (reference)
        # If match, take that entire row and write it into the output file
        for line in sourceReader:
            #print("now viewing: this line")
            if line[1] in geneList and float(line[2]) > 0:
                #print("It's a match!")
                #print("line is",line)
                geneName = geneList[line[1]]
                geneInfo = geneDescriptions[line[1]]
                newRow = [str(line[0])] + line[1:] + [geneName, geneInfo]
                cardioGenesWriter.writerow(newRow)

    print("Anaysis complete")


# main, etc
if __name__ == '__main__':
    main()
