import pandas as pd
import sys

def select_db_isolate(isolatename):
    print(isolatename)
    f1 = open('../../result/'+isolatename+'/' +  isolatename+'-select-cluster-identity_all.txt','r')
    data1=f1.readlines()
    f1.close()
    
    isolateidentity_db_cluster_select = [] #top5
    isolatename_db_cluster_select = [] #top5
    isolatecount_db_cluster_select = []
    isolateaverage_db_cluster_select = [] #top5
    isolateaverage_2_db_cluster_select = [] #top5
    listcount_db_cluster_select = []
    
    k = 0
    for line1 in data1:
        y = line1.split("\n")
        cluster= y[0]
                
        f2 = open('../../result/'+isolatename+'/' +  isolatename+'-'+'cluster'+ cluster +'_pan_genome_reference_count.txt','r')
        data2=f2.readlines()
        f2.close()
        
        fcount = open('../../cluster/cluster'+cluster+'/pan_gene_count.txt','r')
        list_count=fcount.readlines()
        fcount.close()
        
        isolateidentity_db_cluster = [] #
        isolatename_db_cluster = [] #
        isolatecount_db_cluster = []
        isolateaverage_db_cluster = [] #
        isolateaverage_2_db_cluster = [] #
        listcount_db_cluster = [] #
        
        f3 = open('../../result/'+isolatename+'/' +  isolatename+'-'+'cluster'+ cluster +'_pan_genome_reference_count_avg.txt','w')
        
        j = 0
        j = 0
        for line2 in data2:
            m = line2.split("\n")
            n = m[0].split(" ")
            
            listcount = list_count[j].split("\n")
            
            f3.write(str(n[0]))
            f3.write(' ')
            f3.write(str('{:.2f}'.format(n[3])))
            f3.write(' ')
            f3.write(str('{:.0f}'.format(listcount[0])))
            f3.write(' ')
            f3.write(str('{:.2f}'.format(float(n[3])/float(listcount[0]))))
            f3.write('\n')
            
            
            if float(n[2]) == 0:
                j = j+1
                continue
            isolateidentity_db_cluster.append(n[3])
            isolatename_db_cluster.append(n[0])
            isolatecount_db_cluster.append(n[2])
            isolateaverage_db_cluster.append(float(n[3])/float(n[2]))
            isolateaverage_2_db_cluster.append(float(n[3])/float(listcount[0]))
            listcount_db_cluster.append(float(listcount[0]))
            j = j +1
        
        f3.close()
        
        
        
        sorted_id = sorted(range(len(isolateidentity_db_cluster)), key = lambda x:isolateidentity_db_cluster[x], reverse=True)
                               
        for i in range(len(sorted_id)):
            if i > 5:
                break
            isolateidentity_db_cluster_select.append(isolateidentity_db_cluster[sorted_id[i]])
            isolatename_db_cluster_select.append(isolatename_db_cluster[sorted_id[i]])
            isolatecount_db_cluster_select.append(isolatecount_db_cluster[sorted_id[i]])
            isolateaverage_db_cluster_select.append(isolateaverage_db_cluster[sorted_id[i]])
            isolateaverage_2_db_cluster_select.append(isolateaverage_2_db_cluster[sorted_id[i]])
            listcount_db_cluster_select.append(listcount_db_cluster[sorted_id[i]])
        k = k+1
        print(k)
        if k == 6:
            break
        
    sorted_id_all = sorted(range(len(isolateaverage_db_cluster_select)), key = lambda x:isolateaverage_db_cluster_select[x], reverse=True)    
    
    isolateidentity_db_cluster_final = [] #top5
    isolatename_db_cluster_final = [] #top5
    isolatecount_db_cluster_final = []
    isolateaverage_db_cluster_final = [] #top5
    isolateaverage_2_db_cluster_final = [] #top5
    listcount_db_cluster_final = [] #top5
    
    
    for i in range(len(sorted_id_all)):
        isolateidentity_db_cluster_final.append(isolateidentity_db_cluster_select[sorted_id_all[i]])
        isolatename_db_cluster_final.append(isolatename_db_cluster_select[sorted_id_all[i]])
        isolatecount_db_cluster_final.append(isolatecount_db_cluster_select[sorted_id_all[i]])
        isolateaverage_db_cluster_final.append(isolateaverage_db_cluster_select[sorted_id_all[i]])
        isolateaverage_2_db_cluster_final.append(isolateaverage_2_db_cluster_select[sorted_id_all[i]])
        listcount_db_cluster_final.append(listcount_db_cluster_select[sorted_id_all[i]])
    
    isolatename_db_cluster_final_pd = {'sequencing_id':isolatename_db_cluster_final}
    isolatename_db_cluster_final_pd_1 = pd.DataFrame(isolatename_db_cluster_final_pd)
    
    
    data_all_genome = pd.read_table('../../cluster/1187_all_genomes_new.txt',sep='	')
    match = isolatename_db_cluster_final_pd_1.merge(data_all_genome, on='sequencing_id')
    print(match.shape[1])
    
    f3 = open('../../result/'+isolatename+'/' + isolatename +'-select-db-isolate-average.txt','w')
    for i in range(match.shape[0]):
        f3.write(str(isolatename_db_cluster_final[i]))
        f3.write("	")
        f3.write(str('{:.2f}'.format(isolateidentity_db_cluster_final[i])))
        f3.write("	")
        f3.write(str('{:.0f}'.format(isolatecount_db_cluster_final[i])))
        f3.write("	")
        f3.write(str('{:.2f}'.format(isolateaverage_db_cluster_final[i])))
        f3.write("	")
        f3.write(str('{:.2f}'.format(isolateaverage_2_db_cluster_final[i])))
        f3.write("	")
        f3.write(str('{:.0f}'.format(listcount_db_cluster_final[i])))
        f3.write("	")
        for j in range(match.shape[1]-1):
            if j==0:
                continue
            f3.write(str(match.iloc[i,j]))
            f3.write("	")
        f3.write(str(match.iloc[i,match.shape[1]-1]))
        if i == match.shape[0]-1:
            print(i)
            continue
        f3.write("	")
    f3.close() 
    
arg=sys.argv
print(arg)

select_db_isolate(arg[1])

