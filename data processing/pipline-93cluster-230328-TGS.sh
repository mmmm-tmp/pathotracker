# main pipeline for PathoTracker (TGS)
pwd
date
echo ${1}
isolate=${1}
identity_virulence=${2}
identity_antimicrobial=${3}
coverage_virulence=${4}
coverage_antimicrobial=${5}
reads_type_value=${6}

echo ${1} ${2} ${3} ${4} ${5} ${6}


mkdir ../../result/${isolate}
mv ../../upload/${isolate}.fasta ../../result/${isolate}/

sh ../../pipline/pubdb.sh ${1} ${2} ${3} ${4} ${5} &


# #blast
for i in {1..93}; do
	blastn -query ../../pan_genome_ref/cluster${i}_pan_genome_reference.fasta -subject ../../result/${isolate}/${isolate}.fasta -outfmt '7 qseqid qlen sseqid slen pident length mismatch gaps qstart qend sstart send evalue bitscore qcovs qcovus'  > ../../result/${isolate}/${isolate}-cluster${i}.bls
done

# #get_cov_80
for i in {1..93}; do
	python3 ../../pipline/cat_all_cov_gene-93cluster.py ${isolate}-cluster${i} ${isolate} ${i}
done

# # #get_best_cluster
python3 ../../pipline/select-cluster-93cluster.py ${isolate}

# # #get_best_isolate

i=0
cat ../../result/${isolate}/${isolate}-select-cluster-identity_all.txt | 
	while read cluster ; do 
		echo ${isolate}
		echo ${cluster}
		python3 ../../piplineget_best_isolate.py ${isolate} cluster${cluster}
		if ((i>4)); then
                break
        	fi
        	((i=i+1))
        	echo ${i}	
done


#get_genome_infomation

python3 ../../pipline/select_db_isolate-93cluster_average-TGS.py ${isolate}

date


