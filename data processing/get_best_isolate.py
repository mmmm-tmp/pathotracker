# encoding: utf-8
import numpy as np
import sys
import os


def select_NM(isolate_name1, isolate_name, dict_pan_NM, dict_pan_read_count, dict_pan_name,data1, isolatename, clustername):    
    for line in data1:
        data2 = line.split('\n')
        x = data2[0].split(" ")
        
        for j in range(len(dict_pan_name[isolate_name])):
            if dict_pan_name[isolate_name][j] in x[0]: 
                dict_pan_NM[isolate_name] = dict_pan_NM[isolate_name] +float(x[3]) 
                dict_pan_read_count[isolate_name] = dict_pan_read_count[isolate_name] + 1
                break
                
    f3 = open('../../result/'+isolatename+'/' +isolatename+'-' + clustername +'_pan_genome_reference_count.txt','a')
    f3.write(str(isolate_name1))
    f3.write(' ')
    f3.write(str(isolate_name))
    f3.write(' ')
    f3.write(str(dict_pan_read_count[isolate_name]))
    f3.write(' ')
    f3.write(str(dict_pan_NM[isolate_name]))
    f3.write('\n')
    f3.close()


def getinformation(isolatename, clustername):
    blsname =  isolatename + '-' + clustername +'-all-cov-gene-80'
    
    fpan = open('../../cluster/'+clustername+'/list_pan_roary.txt','r')
    list_pan=fpan.readlines()
    fpan.close()

    fname = open('../../cluster/'+clustername+'/list_isolate_name.txt','r')
    list_name=fname.readlines()
    fname.close()

    X_pan = []
    X_name = []
    dict_pan_NM={}
    dict_pan_read_count={}
    dict_pan_name={}
    
    for line in list_pan:
        line = line.strip('\n') 
        
        X_pan.append(line)
        dict_pan_NM[line] = 0
        dict_pan_read_count[line] = 0
        
        f_isolate_pan = open('../../cluster/' + clustername +'/'+ line +'.txt','r')
        list_isolate_pan=f_isolate_pan.readlines()
        f_isolate_pan.close()
        dict_pan_name[line]=[]
        for line2 in list_isolate_pan:
            line2 = line2.strip('\n') 
            dict_pan_name[line].append(line2)

    for line in list_name:
        line = line.strip('\n') 
        X_name.append(line)
        
    f1 = open('../../result/'+isolatename+'/' + blsname+'.txt','r')
    data1=f1.readlines()
    f1.close()
    print('read bls file over!')
    for i in range(len(X_pan)):
        isolate_name = X_pan[i]
        isolate_name1 = X_name[i]
        dict_pan_NM[isolate_name] = 0
        dict_pan_read_count[isolate_name] = 0        
        select_NM(isolate_name1, isolate_name, dict_pan_NM, dict_pan_read_count, dict_pan_name, data1, isolatename, clustername)


arg=sys.argv
print(arg)
getinformation(arg[1], arg[2])
    
