for sp in {1..93}; do
        cd ./cluster${sp}
        python panname_from_csv.py gene_presence_absence.csv
        cd ..
done