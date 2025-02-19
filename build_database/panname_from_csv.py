#import numpy as np
import sys
def count_pan_genes(pathtocsv):

    f1 = open(pathtocsv,'r')
    data1=f1.readlines()
    f1.close()
    print("read over!")

    f2 = open('./list_pan_roary.txt','w')
    tag = 0
    for line in data1:
        data2 = line.split('\n')
        x = data2[0].split(",\"")
        if tag == 0:
            tag = tag + 1
            continue
        for i in range(len(x)):
            if i < 14:
                continue
            y = x[i].split("    ")
            y = y[0].split(" ")
            z = y[0].split("\"")

            k = z[0].split('_')[-1]
            m = z[0].split('_'+k)
            f2.write(m[0])
            f2.write('\n')
        tag = tag + 1
        if tag == 2:
            break

    f2.close()

arg=sys.argv
print(arg)

pathtocsv=arg[1]
count_pan_genes(pathtocsv)
