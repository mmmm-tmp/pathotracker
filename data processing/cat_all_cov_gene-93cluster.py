import sys

def cat_qcovus(isolateclusteri,isolate,cluster):
    print(isolateclusteri)
    f1 = open('../../result/'+isolate+'/'+ isolateclusteri+'.bls','r')
    data1=f1.readlines()
    f1.close()

    f2 = open('../../result/'+isolate+'/'+ isolateclusteri +'-all-cov-gene-80.txt','a')
    f3 = open('../../result/'+isolate+'/'+isolate+'-cluster-all-cov-gene-80.txt','a')
    count_gene = 0
    identity_all = 0
    identity_cov = 0
    tag = 0
    for line in data1:
        data2 = line.split()
        if data2[0][0].isalpha():
            x = line.split("	") 
            if int(x[14]) < 80:
                continue
            tag = 1
            line1 = x[0]
            line2 = x[14]
            if int(line2) > cov:
                cov = int(line2)
                identity = x[4]
        else:
            if tag == 1:
                count_gene = count_gene +1
                f2.write(line1)
                f2.write(" ")
                f2.write(identity)
                f2.write(" ")
                f2.write(str(cov))
                f2.write(" ")
                f2.write(str(cov*float(identity)/100))
                f2.write("\n")
                identity_all = identity_all + float(identity)
                identity_cov = identity_cov + cov*float(identity)
            tag = 0
            cov = 0
            continue
    f2.close()  
    f3.write(str(cluster))
    f3.write(" ")
    f3.write(str(count_gene))
    f3.write(" ")
    f3.write(str(identity_all))
    f3.write(" ")
    if count_gene == 0:
        f3.write("\n")
        return 0
    f3.write(str(identity_all/count_gene))
    f3.write(" ")
    f3.write(str(identity_cov/count_gene/100))
    f3.write("\n")
    
    f3.close()

arg=sys.argv
print(arg)

cat_qcovus(arg[1],arg[2],arg[3])
