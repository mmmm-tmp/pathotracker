# encoding: utf-8

def count_pan_genes():
    global gene
    global isolate
    f1 = open('gene_presence_absence.csv','r')
    data1=f1.readlines()
    f1.close()
    print("read over!")
    f3 = open('./pan_gene_count.txt','w')
    for i in range(len(isolate)):
        f2 = open('./'+ isolate[i] +'.txt','w')
        isolate_gene = 0
        for line in data1:
            data2 = line.split('\n')
            for j in range(len(gene)):
                if gene[j] in data2[0]:
                    x = data2[0].split("\",\"") 
                    x[len(x)-1] = x[len(x)-1].strip("\"") #
                    if '' != x[14+i]:
                        isolate_gene = isolate_gene+1
                        f2.write(gene[j])
                        f2.write('\n')
                    break
        print(isolate[i],' pan_gene_count:',isolate_gene)
        f3.write(str(isolate_gene))
        f3.write('\n')
        f2.close()
        f2.close()
    f3.close()

fpan = open('./pan_gene_list.txt','r')
list_pan=fpan.readlines()
fpan.close()

gene = []
for line in list_pan:
    line = line.strip('\n') 
    gene.append(line)

fisolate = open('./list_pan_roary.txt','r')
list_isolate=fisolate.readlines()
fisolate.close()

isolate = []
for line in list_isolate:
    line = line.strip('\n') 
    isolate.append(line)

count_pan_genes()