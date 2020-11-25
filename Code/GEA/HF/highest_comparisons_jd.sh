#!/bin/bash

# Produces 3 new output files per sample (input) file:
# 1. All gene IDs sorted by TPM (sort_genes_by_TPM.py)
# 2. Cardiovascular genes present in sample
#    (compare_genes.py with cardio reference file)
# 3. Heart failure genes present in sample
#    (compare_genes.py with heart failure reference file)


# Usage:
# $ ./highest_comparisons.sh /path/to/sample results/Sorted_Directory results/Compared_Directory

DATADIR="$1"
RESULTSDIR="$2"
OUTPUTDIR="$3"
SCRIPTDIR=/Users/jinhd/Desktop/ZA_rotation

CARDIOGENES=/Users/jinhd/Desktop/ZA_rotation/genes_of_interest/genes_cardiovascular_06052020_za.csv
HFGENES=/Users/jinhd/Desktop/ZA_rotation/genes_of_interest/genes_heart_failure_06052020_za.csv

mkdir "$RESULTSDIR"

# For every file in a folder (can do with variables I guess?)
for file in "$DATADIR"/*; do
    # run sort_genes_by_TPM.py
    echo "Now sorting $file"
    python "$SCRIPTDIR"/sort_genes_by_TPM.py "$file" "$RESULTSDIR"
done

# Make a new directory for the gene comparisons
mkdir "$OUTPUTDIR"
# cd ./comparisons

# For every new "sorted" output file run the comparison scripts
for f in "$RESULTSDIR"/*; do
    # run compare_genes.py
    echo "Now comparing $f to cardiovascular genes"
    python "$SCRIPTDIR"/compare_genes.py "$f" "$CARDIOGENES" "$OUTPUTDIR"

    echo "Now comparing $f to heart failure genes"
    python "$SCRIPTDIR"/compare_genes.py "$f" "$HFGENES" "$OUTPUTDIR"
done
