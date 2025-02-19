def count_pan_genes(pathtocsv):

    f1 = open(pathtocsv,'r')
    data1=f1.readlines()
    f1.close()
    print("read over!")

    f2 = open('./list_isolate_name.txt','w')
    tag = 0
    for line in data1:
        data2 = line.split('\n')
        x = data2[0].split(",\"")
        for i in range(len(x)):
            if i < 14:
                continue
            z = x[i].split("\"")
            print(z[0])
            f2.write(z[0])
            f2.write('\n')
        tag = tag + 1
        if tag == 1:
            break

    f2.close()

pathtocsv="gene_presence_absence.csv"
count_pan_genes(pathtocsv)
