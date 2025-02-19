for sp in {1..93}; do
        cd ./cluster${sp}
        cat cluster${sp}_pan_genome_reference.fasta | awk '{if($0~/>/) print $0}' > pan_gene_list.txt
        awk '{print $1}' pan_gene_list.txt > pan_gene_list-.txt
        mv pan_gene_list-.txt pan_gene_list.txt
        awk -F '>' '{print$2}' pan_gene_list.txt > pan_gene_list-.txt
        mv pan_gene_list-.txt pan_gene_list.txt
        cd ..
done
