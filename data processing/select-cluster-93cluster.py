import sys

def select_cluster(isolatename):
    print(isolatename)
    f1 = open('../../result/'+isolatename+'/'+isolatename+'-cluster-all-cov-gene-80.txt','r')
    data1=f1.readlines()
    f1.close()
    identity_all = []
    cluster = []
    
    for line in data1:
        y = line.split("\n")
        x = y[0].split(" ")
        cluster.append(x[0])
        if len(x) < 5:
            identity_all.append(x[2])
        else:
            identity_all.append(x[3])
    
    sorted_id = sorted(range(len(identity_all)), key = lambda x:identity_all[x], reverse=True)

    
    f2 = open('../../result/'+isolatename+'/' +isolatename+'-select-cluster-identity_all.txt','w')
    for i in range(len(sorted_id)):
        f2.write(str(cluster[sorted_id[i]]))
        f2.write("\n")
    f2.close() 

arg=sys.argv
print(arg)

select_cluster(arg[1])
