# compare with VFDB and Resfinder
date
isolate=${1}
identity_virulence=${2}
identity_antimicrobial=${3}
coverage_virulence=${4}
coverage_antimicrobial=${5}

blastn -query ../../database/VFDB_nt.fasta -subject ../../result/${isolate}/${isolate}.fasta -outfmt '7 qseqid qlen sseqid slen pident length mismatch gaps qstart qend sstart send evalue bitscore qcovs qcovus'  > ../../result/${isolate}/${isolate}-VFDB.bls
blastn -query ../../database/resfinder.fasta -subject ../../result/${isolate}/${isolate}.fasta -outfmt '7 qseqid qlen sseqid slen pident length mismatch gaps qstart qend sstart send evalue bitscore qcovs qcovus'  > ../../result/${isolate}/${isolate}-resfinder.bls

python ../../pipline/pubdb.py ${isolate}-VFDB ${isolate} ${identity_virulence} ${coverage_virulence}
python ../../pipline/pubdb.py ${isolate}-resfinder ${isolate} ${identity_antimicrobial} ${coverage_antimicrobial}

date
