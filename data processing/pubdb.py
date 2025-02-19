import sys

def cat_qcovus(filename,isolate,identity,coverage):
    print(filename)
    f1 = open('../../result/'+isolate+'/'+ filename+'.bls','r')
    data1=f1.readlines()
    f1.close()
    
    f2 = open('../../result/'+isolate+'/'+ filename+'_filter.txt','w')
    count_gene = 0
    tag = 0
    for line in data1:
        data2 = line.split()
        if data2[0][0].isalpha():
            x = line.split("	") 
            if int(x[14]) < float(coverage)*100:
                continue
            if float(x[4]) < float(identity)*100:
                continue
            tag = 1
            line1 = x[0]
            cov = x[14]
            ident = x[4]
        else:
            if tag == 1:
                count_gene = count_gene +1
                f2.write(line1)
                f2.write(" ")
                f2.write(ident)
                f2.write(" ")
                f2.write(cov)
                f2.write(" ")
                f2.write(str(int(cov)*float(ident)/100))
                f2.write(" ")
            tag = 0
            continue
    f2.close()  
    f3 = open('../../result/'+isolate+'/'+ filename+'.txt','w')
    f3.write(str(count_gene))
    f3.close()  


arg=sys.argv
print(arg)

cat_qcovus(arg[1],arg[2],arg[3],arg[4])
