###annotate fasta file, get gff files
prokka --mincontiglen 100 --prefix $sample $sample.fasta --force

##run roary (both run on all isolates in database and on each cluster)
roary -e -s --mafft -p 16 --group_limit 60000  *.gff -f $wdir1/$out -

##run iqtree
./iqtree-2.2.2.2-Linux/bin/iqtree2 -s $wdir/${name}.fasta  -nt AUTO -b 100 -m GTR+G+I

##run Treecluster 
python3 TreeCluster.py -i treefile -m sum_branch -t 0.015 >result-sum_branch_0015.txt

##generate pan gene list
sh pan_gene_list_generate.sh
sh panname_from_csv.sh
sh generate_pan_count.sh
sh isolatename_from_csv.sh




