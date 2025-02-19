# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import View
import os
from django.shortcuts import redirect
#from django.urls
from time import sleep
import time
import threading
import re
import subprocess
from django.http import HttpResponse, Http404, StreamingHttpResponse
from pathlib import *
import random

#log
import logging
error_logger = logging.getLogger('PathoTracker_error')

# Create your views here.

class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
    def run(self):
        time.sleep(2)
        self.result = self.func(*self.args)
    def get_result(self):
        threading.Thread.join(self)  # 
        try:
            return self.result
        except Exception:
            return None



def index(request):
    return render(request,"demo1/huilab-index.html")

def home(request):
    return render(request,"demo1/huilab-index.html")

def Tutorial(request):
    #print("Tutorial")
    return render(request,"demo1/Tutorial.html")

def Disclaimer(request):
    #print("Disclaimer")
    return render(request,"demo1/Disclaimer.html")

def About_Contact(request):
    #print("About")
    return render(request,"demo1/About.html")

def Wrong(request):
    #print("Wrong")
    return render(request,"demo1/Wrong.html")

def CRE_network(request):

    return render(request,"demo1/CRE_network.html")

def PathoTracker(request):
    #print("PathoTracker")
    return render(request,"demo1/PathoTracker.html")

def PathoTracker_ST11(request):
    #print("PathoTracker")
    return render(request,"demo1/PathoTracker_ST11.html")

def phylogenetic_tree(request):
    #print("phylogenetic_tree")
    return render(request,"demo1/phylogenetic_tree.html")


def result(request, filename):
    #print(request.method)
    
    #print("result")
    
    species = ""
    try:
        file = open("../../result/" + filename + "/" + filename + "-filtlong-report-.tsv", 'r')
        species = file.read()
        file.close()
        species = species.split("\n")
        species = species[0]
    except OSError:
        print('no species content')
    
    file = open("../../result/"+filename + "/"+ filename +"-select-db-isolate-average-3_1101.txt", 'r')
    #message = file.readlines()
    message = file.read()
    #print(message)
    file.close()
    file = open("../../result/"+filename + "/"+ filename +"-resfinder_filter.txt", 'r')
    message_res = file.read()
    file.close()
    file = open("../../result/"+filename + "/"+ filename +"-resfinder.txt", 'r')
    count_res = file.read()
    file.close()
    file = open("../../result/"+filename + "/"+ filename +"-VFDB_filter.txt",'r')
    message_vir = file.read()
    file.close()
    file = open("../../result/"+filename + "/"+ filename +"-VFDB.txt", 'r')
    count_vir = file.read()
    file.close()
    
    # filename = filename.split("_")
    # filename = filename[0]
    
    return render(request, "demo1/Result.html",{"filename":filename,"species":species, "html_data":message, "message_res":message_res, "count_res":count_res, "message_vir":message_vir, "count_vir":count_vir})


def running(filename, identity_virulence, identity_antimicrobial, coverage_virulence, coverage_antimicrobial, reads_type_value, sample_type_value):
    #print('running')
    #sleep(11)
    process_result = ''
    
    if reads_type_value == 0 and sample_type_value == 0: # fasta and mNGS_TGS or culture_TGS or culture_NGS
        process_result = subprocess.getoutput("sh ../../pipline/pipline-93cluster-TGS.sh %s %s %s %s %s %s" % (filename, identity_virulence,identity_antimicrobial,coverage_virulence,coverage_antimicrobial,reads_type_value))
    else:
        process_result = subprocess.getoutput("sh ../../pipline/pipline-93cluster-NGS.sh %s %s %s %s %s %s" % (filename, identity_virulence,identity_antimicrobial,coverage_virulence,coverage_antimicrobial,reads_type_value))
    process_result=process_result.lower()
    
    
    
    if "error" in process_result or "no such" in process_result:
        f = open("../../result/"+filename + "/"+ filename +"-something-wrong.txt", 'w')
        f.write(process_result)
        f.close()
        
        # 
        file = open("../../result/"+filename + "/"+ "email_value.txt", 'r')
        email_value = file.read()
        file.close()
        email_value = email_value.split('\n')
        email_value =  email_value[0]
        mail_context = "echo -e \"Dear sir/madam, \nThere is something wrong in your upload file....  \n\nPlease contact the administrator for details.  \n\nYours sincerely, \nPathoTracker webserver \nWe welcome you to join the CRE network and look forward to hearing from you! \nIn case of problems and issues with the services contact the helpdesk huilab_pkuph@163.com\n\" | mailx -v -s \"PathoTracker: Job wrong condition\" %s"% (email_value)
        os.system(mail_context)
    else:
        process_result_mail = subprocess.getoutput("sh ../../pipline/pipline-93cluster-mail.sh %s" % (filename))
    
    
    
def waiting_page(request,filename):
    #print('waiting_page')
    #print(filename)
    return render(request, "demo1/Waiting.html", {"filename":filename})

def waiting(request):
    #print('in waiting def')
    #print(request.body)
    #print(request.POST.getlist('filename'))
    sleep(2)
    
    filename = str(request.POST.getlist('filename'))
    #print(filename)
    filename = filename.split('[\'')
    filename = filename[1].split('\']')
    #print(filename)
    filename = filename[0]
    #print(filename)
    
    if os.path.exists("../../result/"+filename + "/"+ filename +"-something-wrong.txt") == True:
        return HttpResponse("something_wrong") 
    
    if os.path.exists("../../result/"+filename + "/"+ filename +"-select-db-isolate-average-3_1101.txt") == False:  #这个while确保了返回值一直是None
        sleep(300) #sleep 5 min 
        return HttpResponse("Not over")  #应该加一个三天
    else:
        #print("over!")
        return HttpResponse("over")


def handle_uploaded_file(f_obj,i,save_data_value,country_value, email_value,
                            identity_virulence, identity_antimicrobial, coverage_virulence, coverage_antimicrobial, reads_type_value, sample_type_value):
    name = f_obj.name
    name1 = name.split(".")
    filename = name1[0]
    checkname = re.findall("[^a-zA-Z0-9]",filename)
    if len(checkname) > 0 or len(filename) == 0:
        return False,filename
    #print(name1[0])
    
    filename = filename + "_"+ str(random.randint(1,10))
    if reads_type_value == 0:
        writefilename = filename + '.fasta'
    elif reads_type_value == 1 and sample_type_value == 2:
        writefilename = filename + '.r' + str(i) +'.fq.gz'  #双端
    else:
        writefilename = filename + '.fq.gz'
    #print("writefilename",writefilename)
    destination = open("../../upload/"+ writefilename, 'wb+') #
    for chunk in f_obj.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    destination = open("../../database_upload/"+ writefilename, 'wb+')
    for chunk in f_obj.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    if save_data_value == 'yes':
        save_data_value_tmp = 1
    else:
        save_data_value_tmp = 0
    #由于城市之类的中间有空格，所以
    subprocess.getoutput("echo \"%s;%s;%s;%s;%s;%s;\" >> ../../database_upload/list_upload_info.txt" % 
                (writefilename,save_data_value_tmp,reads_type_value,country_value, email_value)) #%s;%s;%s;  
    
    subprocess.getoutput("mkdir ../../result/%s" % (filename))
    subprocess.getoutput("echo \"%s\" >> ../../result/%s/email_value.txt" % (email_value, filename))
    
    running_thread = threading.Thread(target=running, name=filename, 
        args=(filename, identity_virulence, identity_antimicrobial, coverage_virulence, coverage_antimicrobial, reads_type_value, sample_type_value))
    running_thread.start()
    
    return True,filename



def post(request):
    identity_virulence = str(request.POST.getlist('identity_virulence'))
    identity_virulence = identity_virulence.split('\'')
    identity_virulence = identity_virulence[1].split('%')
    identity_virulence = float(identity_virulence[0]) / 100
    #print(identity_virulence)
    identity_antimicrobial = str(request.POST.getlist('identity_antimicrobial'))
    identity_antimicrobial = identity_antimicrobial.split('\'')
    identity_antimicrobial = identity_antimicrobial[1].split('%')
    identity_antimicrobial = float(identity_antimicrobial[0]) / 100
    #print(identity_antimicrobial)
    coverage_virulence = str(request.POST.getlist('coverage_virulence'))
    coverage_virulence = coverage_virulence.split('\'')
    coverage_virulence = coverage_virulence[1].split('%')
    coverage_virulence = float(coverage_virulence[0]) / 100
    #print(coverage_virulence)
    coverage_antimicrobial = str(request.POST.getlist('coverage_antimicrobial'))
    coverage_antimicrobial = coverage_antimicrobial.split('\'')
    coverage_antimicrobial = coverage_antimicrobial[1].split('%')
    coverage_antimicrobial = float(coverage_antimicrobial[0]) / 100
    #print(coverage_antimicrobial)
    reads_type = str(request.POST.getlist('reads_type'))
    #print(reads_type)
    reads_type = reads_type.split('[\'')
    reads_type = reads_type[1].split('\']')
    #print(reads_type)
    reads_type = reads_type[0]
    #print(reads_type)
    if reads_type == 'Assembled or Draft Genome/Contigs':
        reads_type_value = 0
    else:
        reads_type_value = 1
    #print(reads_type_value)

    sample_type = str(request.POST.getlist('sample_type'))
    sample_type = sample_type.split('\'')
    sample_type = sample_type[1]
    if sample_type == 'mNGS_TGS':
        sample_type_value = 0
    elif sample_type == 'culture_TGS':
        sample_type_value = 1
    else:
        sample_type_value = 2 #culture_NGS
    #print(sample_type_value)

    country_value = str(request.POST.getlist('country_value'))
    country_value = country_value.split('\'')
    country_value = country_value[1]
    #print(country_value)
    email_value = str(request.POST.getlist('email'))
    email_value = email_value.split('\'')
    email_value = email_value[1]
    #print(email_value)
    save_data_value = str(request.POST.getlist('save_data_value'))
    save_data_value = save_data_value.split('\'')
    save_data_value = save_data_value[1]
    #print(save_data_value)

    #print(request.FILES.getlist('file'))
    file = request.FILES.getlist('file')
    #print(len(file))
    i = 1
    if len(file) > 0:
        for file_i in file:
            #name = file_i.name
            #print(name)
            #filename = file_i.name
            checknamevalue,filename = handle_uploaded_file(file_i,i,save_data_value,country_value,email_value,
                                identity_virulence, identity_antimicrobial, coverage_virulence, coverage_antimicrobial, reads_type_value, sample_type_value) 
            if checknamevalue==False:
                return HttpResponse("Wrong_file_name")
                #return render(request, "demo1/PathoTracker.html",{"filename":filename,"condition":"Wrong_file_name"})
            i = i + 1
        return HttpResponse(filename)
        #print(checknamevalue," ",filename)
        #return render(request, "demo1/PathoTracker.html",{"filename":filename,"condition":"exist"})
    else:
        return HttpResponse("No_file")
        #return render(request, "demo1/PathoTracker.html",{"filename":filename,"condition":"No_file"})

def test_sequence(request):
    #print('test_sequence')
    try:
        response = StreamingHttpResponse(open('../example/example_sequence_format.txt', 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename('../example/example_sequence_format.txt')
        return response
    except Exception:
        raise Http404  


def test_sequence_CMg(request):
    #print('test_sequence')
    try:
        response = StreamingHttpResponse(open('../example/BAL177_example.fasta', 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename('../example/BAL177_example.fasta')
        return response
    except Exception:
        raise Http404  



########################################generate tree
from io import BytesIO
import matplotlib.pyplot as plt
import base64

def tree_result(request,pathname):
    treefile = "../../phylogenetic_tree_upload/"+ pathname + '/core_gene_alignment.aln.treefile'
    
    file = open("../../phylogenetic_tree_upload/"+pathname + "/"+ "email_value.txt", 'r')
    email_value = file.read()
    file.close()
    email_value = email_value.split('\n')
    email_value =  email_value[0]
    mail_context = "echo \"Dear sir/madam, \nYour job %s has finished on our PathoTracker server. \nYou may visit the results in http://PathoTracker.pku.edu.cn/tree_result/%s  \nYours sincerely, \nPathoTracker webserver \nWe welcome you to join the CRE network and look forward to hearing from you! \nIn case of problems and issues with the services contact the helpdesk huilab_pkuph@163.com\n\" | mailx -v -s \"PathoTracker: Job %s finished\" -a %s %s"% (pathname, pathname, pathname,treefile, email_value)
    #os.system("echo \"Tree file\" | mailx -v -s \"PathoTracker_phylogenetic_tree_analysis\" -a %s %s"% (treefile, "huilab_pkuph@163.com"))
    os.system(mail_context)
    
    #show image
    #image = plt.imread(tree_path_name + 'show_tree.jpg')
    image = plt.imread("../../phylogenetic_tree_upload/"+ pathname + "/show_tree.jpg")
    fig = plt.figure()
    plt.imshow(image)
    plt.show()
    img_stringio = BytesIO()
    fig.savefig(img_stringio, format='jpg')
    img_stringio.seek(0)
    graph = base64.b64encode(img_stringio.getvalue()).decode()
    #graph = img_stringio.getvalue()
    context = {}
    context['graph'] = graph  # 
    context['pathname'] = pathname
    return render(request, "demo1/Result_tree.html", context=context)

def tree_result_download(request,pathname):
    try:
        response = StreamingHttpResponse(open("../../phylogenetic_tree_upload/"+pathname+'/iqtree/core_gene_alignment.aln.treefile', 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename("../../phylogenetic_tree_upload/"+pathname+'/core_gene_alignment.aln.treefile')
        return response
    except Exception:
        raise Http404  #

def tree_waiting_page(request,pathname):
    #print('waiting_page_tree')
    return render(request, "demo1/Waiting_tree.html", {"pathname":pathname})

def tree_waiting(request):
    #print('in tree waiting def')
    pathname = str(request.POST.getlist('pathname'))
    #print(pathname)
    pathname = pathname.split('[\'')
    pathname = pathname[1].split('\']')
    #print(pathname)
    pathname = pathname[0]
    #print(pathname)
    
    somethingwrong = os.path.exists("../../phylogenetic_tree_upload/"+pathname+"/"+pathname+"-something-wrong.txt")
    #print("test why "+str(somethingwrong == True))
    if somethingwrong == True:
        #sleep(600)
        #print("in something_wrong")
        return HttpResponse("something_wrong") 
    
    #print(os.path.exists("../../phylogenetic_tree_upload/"+pathname+"/show_tree.jpg"))
    if os.path.exists("../../phylogenetic_tree_upload/"+pathname+"/show_tree.jpg") == False:  #
        sleep(600) #sleep 5 min
        return HttpResponse("Not over")
    else:
        #print("in tree over")
        return HttpResponse("over")


def running_tree(pathname,checknamevalue):
    #print('running tree')
    
    process_result1 = subprocess.getoutput("sh ../../pipline_tree/pipline-tree-1.sh %s" % (pathname))  #所以这个不加后面的是对的
    process_result1 = process_result1.lower()
    process_result2 = subprocess.getoutput("sh ../../pipline_tree/pipline-tree-2.sh %s" % (pathname))
    process_result2 = process_result2.lower()

    if "error" in process_result1 or "no such" in process_result1 or "error" in process_result2 or "no such" in process_result2:
        #print(process_result)
        #print("error")
        f = open("../../phylogenetic_tree_upload/"+pathname + "/"+ pathname +"-something-wrong.txt", 'w+')
        f.write(process_result1)
        f.close()
        
        f = open("../../phylogenetic_tree_upload/"+pathname + "/"+ pathname +"-something-wrong.txt", 'w+')
        f.write(process_result2)
        f.close()
        
        file = open("../../phylogenetic_tree_upload/"+pathname + "/"+ "email_value.txt", 'r')
        email_value = file.read()
        file.close()
        email_value = email_value.split('\n')
        email_value =  email_value[0]
        mail_context = "echo -e \"Dear sir/madam, \nThere is something wrong in your upload file....  \n\nPlease contact the administrator for details.  \n\nYours sincerely, \nPathoTracker webserver \nWe welcome you to join the CRE network and look forward to hearing from you! \nIn case of problems and issues with the services contact the helpdesk huilab_pkuph@163.com\n\" | mailx -v -s \"PathoTracker: Job wrong condition\" %s"% (email_value)
        os.system(mail_context)
    else:
        process_result_mail = subprocess.getoutput("sh ../../pipline_tree/pipline-tree-mail.sh %s" % (pathname))
        

def handle_uploaded_file_tree(f_obj,pathname):
    name = f_obj.name
    name1 = name.split(".")
    filename = name1[0]
    checkname = re.findall("[^a-zA-Z0-9]",filename)
    if len(checkname) > 0 or len(filename) == 0:
        return False,filename #return 0
    #print(name1[0])
    
    name = name1[0]+".fasta"

    isExists = os.path.exists("../../phylogenetic_tree_upload/"+pathname)
    if not isExists:
        os.makedirs("../../phylogenetic_tree_upload/"+pathname)
    destination = open(os.path.join("../../phylogenetic_tree_upload/"+pathname+'/', name), 'wb+')
    for chunk in f_obj.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    
    
    
    return True,pathname


def post_tree(request):

    number_of_sequences = str(request.POST.getlist('number_of_sequences'))
    number_of_sequences = number_of_sequences.split('\'')
    number_of_sequences = number_of_sequences[1]
    number_of_sequences = int(number_of_sequences[0])
    #print(number_of_sequences)

    email_value = str(request.POST.getlist('email'))
    email_value = email_value.split('\'')
    email_value = email_value[1]
    #print(email_value)
    file = request.FILES.getlist('file')
    #print(4444)
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    pathname = timestr + "_"+ str(random.randint(1,10))
    
    #print(len(file))
    if len(file) > 0:
        for file_i in file:
            #name = file_i.name
            #print(name)
            #filename = file_i.name
            checknamevalue,pathname = handle_uploaded_file_tree(file_i,pathname)
            if checknamevalue == False:
                return HttpResponse("Wrong_file_name")

        subprocess.getoutput("echo \"%s;\" >> ../../phylogenetic_tree_upload/%s/email_value.txt" % (email_value, pathname))
        running_thread = threading.Thread(target=running_tree, name=pathname, args=(pathname, checknamevalue))
        running_thread.start()
        
        return HttpResponse(pathname)
    else:
        return HttpResponse("No_file")






###########################################join cre
def join_cre(request):
    affiliation_value = str(request.POST.getlist('affiliation'))
    affiliation_value = affiliation_value.split('\'')
    affiliation_value = affiliation_value[1]
    #print(affiliation_value)

    institution_value = str(request.POST.getlist('institution'))
    institution_value = institution_value.split('\'')
    institution_value = institution_value[1]
    #print(institution_value)

    name_value = str(request.POST.getlist('name'))
    name_value = name_value.split('\'')
    name_value = name_value[1]
    #print(name_value)

    country_value = str(request.POST.getlist('country'))
    country_value = country_value.split('\'')
    country_value = country_value[1]
    #print(country_value)

    city_value = str(request.POST.getlist('city'))
    city_value = city_value.split('\'')
    city_value = city_value[1]
    #print(city_value)

    process_result = subprocess.getoutput("echo %s %s %s %s %s >> ../../database_upload/list_join_CRE.txt" % (affiliation_value,institution_value,name_value,country_value,city_value))  # 所以这个不加后面的是对的
    process_result = process_result.lower()
    if "error" in process_result or "no such" in process_result:  # 
        return HttpResponse('error')
    return HttpResponse('success')



###########################################species detection

def result_species(request, filename):

    file = open("../../result/" + filename + "/" + filename + "-filtlong-report-.tsv", 'r')
    species = file.read()
    file.close()
    species = species.split("\n")
    species = species[0]

    return render(request, "demo1/Result_species.html",{"filename":filename,"species":species})

def species_waiting_page(request,filename):
    #print('waiting_page')
    #return render(request, "demo1/Waiting_species.html")
    return render(request, "demo1/Waiting_species.html", {"filename":filename})

def species_waiting(request):
    #print('in waiting def')
    filename = str(request.POST.getlist('filename'))
    filename = filename.split('[\'')
    filename = filename[1].split('\']')
    filename = filename[0]
    print(filename)
    
    if os.path.exists("../../result/"+filename + "/"+ filename +"-something-wrong.txt") == True:
        return HttpResponse("something_wrong") 
    
    if os.path.exists("../../result/"+filename + "/"+ filename +"-filtlong-report-.tsv") == False:  #
        sleep(300) #sleep 5 min
        return HttpResponse("Not over")
    else:
        return HttpResponse("over")


def handle_uploaded_file_species(f_obj,save_data_value,country_value,email_value): 
    name = f_obj.name
    name1 = name.split(".")
    filename = name1[0]
    checkname = re.findall("[^a-zA-Z0-9]",filename)
    if len(checkname) > 0 or len(filename) == 0:
        return False,filename
    #print(name1[0])
    
    filename = filename + "_"+ str(random.randint(1,10))
    
    #之后要取消注释
    writefilename = filename + '.fq.gz'
    destination = open("../../upload/" + writefilename, 'wb+') 
    for chunk in f_obj.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    destination = open("../../upload/" + writefilename, 'wb+')
    for chunk in f_obj.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    
    if save_data_value == 'yes':
        save_data_value_tmp = 1
    else:
        save_data_value_tmp = 0
    #由于城市之类的中间有空格，所以
    
    #之后要取消注释
    subprocess.getoutput("echo \"%s;%s;%s;%s;%s\" >> ../../database_upload/list_upload_info_species.txt" % (writefilename,save_data_value, country_value, email_value)) 
    
    subprocess.getoutput("mkdir ../../result/%s" % (filename))
    subprocess.getoutput("echo \"%s\" >> ../../result/%s/email_value.txt" % (email_value, filename))
    
    return True,filename


def running_species(filename,checknamevalue):
    # return redirect("index:shop",permanent=True)

    #print('running')
    
    #需要取消注释
    process_result = subprocess.getoutput("sh ../../pipline_sepcies/pipline-species.sh %s" % (filename))
    process_result=process_result.lower()

    #
    if "error" in process_result or "no such" in process_result:
        print(process_result)
        print("error")
        f = open("../../result/"+filename + "/"+ filename +"-something-wrong.txt", 'w')
        f.write(process_result)
        f.close()
        
        file = open("../../result/"+filename + "/"+ "email_value.txt", 'r')
        email_value = file.read()
        file.close()
        email_value = email_value.split('\n')
        email_value =  email_value[0]
        mail_context = "echo -e \"Dear sir/madam, \nThere is something wrong in your upload file....  \n\nPlease contact the administrator for details.  \n\nYours sincerely, \nPathoTracker webserver \nWe welcome you to join the CRE network and look forward to hearing from you! \nIn case of problems and issues with the services contact the helpdesk huilab_pkuph@163.com\n\" | mailx -v -s \"PathoTracker: Job wrong condition\" %s"% (email_value)
        os.system(mail_context)
    else:
        process_result_mail = subprocess.getoutput("sh ../../pipline_sepcies/pipline-species-mail.sh %s" % (filename))
        

def species(request):
    # return redirect("index:shop",permanent=True)
    #print("Species-detect")
    return render(request,"demo1/Species-detect.html")

def post_species(request):
    country_value = str(request.POST.getlist('country_value'))
    country_value = country_value.split('\'')
    country_value = country_value[1]
    #print(country_value)
    email_value = str(request.POST.getlist('email'))
    email_value = email_value.split('\'')
    email_value = email_value[1]
    #print(email_value)
    save_data_value = str(request.POST.getlist('save_data_value'))
    save_data_value = save_data_value.split('\'')
    save_data_value = save_data_value[1]
    #print(save_data_value)

    file = request.FILES.getlist('file')
    
    checknamevalue,filename = handle_uploaded_file_species(file[0],save_data_value,country_value,email_value) 
    if checknamevalue==False:
        return HttpResponse("Wrong_file_name")
    
    running_thread = threading.Thread(target=running_species, name=filename, args=(filename,checknamevalue))
    running_thread.start()
    
    return HttpResponse(filename)






##########################################PathoTracker ST11
def result_ST11(request, filename): 
    print("in st11 result")
    species = ""
    
    file = open("../../result_ST11/"+filename + "/"+ filename +"-select-db-isolate-average-ST11.txt", 'r')
    #message = file.readlines()
    message = file.read()
    #print(message)
    file.close()
    file = open("../../result_ST11/"+filename + "/"+ filename +"-resfinder_filter.txt", 'r')
    message_res = file.read()
    file.close()
    file = open("../../result_ST11/"+filename + "/"+ filename +"-resfinder.txt", 'r')
    count_res = file.read()
    file.close()
    file = open("../../result_ST11/"+filename + "/"+ filename +"-VFDB_filter.txt",'r')
    message_vir = file.read()
    file.close()
    file = open("../../result_ST11/"+filename + "/"+ filename +"-VFDB.txt", 'r')
    count_vir = file.read()
    file.close()
    
    return render(request, "demo1/Result_ST11.html",{"filename":filename,"species":species, "html_data":message, "message_res":message_res, "count_res":count_res, "message_vir":message_vir, "count_vir":count_vir})


def running_ST11(filename, identity_virulence, identity_antimicrobial, coverage_virulence, coverage_antimicrobial, reads_type_value, sample_type_value):
    #print('running')
    #sleep(11)
    process_result = ''
    
    if reads_type_value == 0 and sample_type_value == 0: # fasta and mNGS_TGS or culture_TGS or culture_NGS
        process_result = subprocess.getoutput("sh ../../pipline_ST11/pipline-41cluster-TGS.sh %s %s %s %s %s %s" % (filename, identity_virulence,identity_antimicrobial,coverage_virulence,coverage_antimicrobial,reads_type_value))
    else:
        process_result = subprocess.getoutput("sh ../../pipline_ST11/pipline-41cluster-NGS.sh %s %s %s %s %s %s" % (filename, identity_virulence,identity_antimicrobial,coverage_virulence,coverage_antimicrobial,reads_type_value))

    process_result=process_result.lower()
    print("finish process~")
    if "error" in process_result or "no such" in process_result:
        f = open("../../result_ST11/"+filename + "/"+ filename +"-something-wrong.txt", 'w')
        f.write(process_result)
        f.close()
        
        # 报错通知
        file = open("../../result_ST11/"+filename + "/"+ "email_value.txt", 'r')
        email_value = file.read()
        file.close()
        email_value = email_value.split('\n')
        email_value =  email_value[0]
        mail_context = "echo -e \"Dear sir/madam, \nThere is something wrong in your upload file....  \n\nPlease contact the administrator for details.  \n\nYours sincerely, \nPathoTracker webserver \nWe welcome you to join the CRE network and look forward to hearing from you! \nIn case of problems and issues with the services contact the helpdesk huilab_pkuph@163.com\n\" | mailx -v -s \"PathoTracker: Job wrong condition\" %s"% (email_value)
        os.system(mail_context)
    else:
        process_result_mail = subprocess.getoutput("sh ../../pipline_ST11/pipline-93cluster-mail.sh %s" % (filename))
    
    
    
def waiting_page_ST11(request,filename):
    #print('waiting_page')
    #print(filename)
    return render(request, "demo1/Waiting_ST11.html", {"filename":filename})

def waiting_ST11(request):
    #print('in waiting def')
    #print(request.body)
    #print(request.POST.getlist('filename'))
    sleep(2)
    
    filename = str(request.POST.getlist('filename'))
    #print(filename)
    filename = filename.split('[\'')
    filename = filename[1].split('\']')
    #print(filename)
    filename = filename[0]
    print(filename)
    
    if os.path.exists("../../result_ST11/"+filename + "/"+ filename +"-something-wrong.txt") == True:
        print("wrong")
        return HttpResponse("something_wrong") 
    
    if os.path.exists("../../result_ST11/"+filename + "/"+ filename +"-select-db-isolate-average-ST11.txt") == False:  #
        sleep(300) #sleep 5 min 
        return HttpResponse("Not over")  #应该加一个三天
    else:
        return HttpResponse("over")


def handle_uploaded_file_ST11(f_obj,i,save_data_value,country_value, email_value,
                            identity_virulence, identity_antimicrobial, coverage_virulence, coverage_antimicrobial, reads_type_value, sample_type_value):
    name = f_obj.name
    name1 = name.split(".")
    filename = name1[0]
    checkname = re.findall("[^a-zA-Z0-9]",filename)
    if len(checkname) > 0 or len(filename) == 0:
        return False,filename
    #print(name1[0])
    
    filename = filename + "_"+ str(random.randint(1,10))
    if reads_type_value == 0:
        writefilename = filename + '.fasta'
    elif reads_type_value == 1 and sample_type_value == 2:
        writefilename = filename + '.r' + str(i) +'.fq.gz'  #双端
    else:
        writefilename = filename + '.fq.gz'
    
    #print("writefilename",writefilename)
    
    destination = open("../../upload_ST11/"+ writefilename, 'wb+') #
    for chunk in f_obj.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    destination = open("../../database_upload_ST11/"+ writefilename, 'wb+')
    for chunk in f_obj.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    if save_data_value == 'yes':
        save_data_value_tmp = 1
    else:
        save_data_value_tmp = 0
    #
    subprocess.getoutput("echo \"%s;%s;%s;%s;%s;%s;\" >> ../../database_upload_ST11/list_upload_info.txt" % 
                (writefilename,save_data_value_tmp,reads_type_value,country_value, email_value)) #%s;%s;%s;  
    
    subprocess.getoutput("mkdir ../../result_ST11/%s" % (filename))
    subprocess.getoutput("echo \"%s\" >> ../../result_ST11/%s/email_value.txt" % (email_value, filename))
    
    running_thread = threading.Thread(target=running_ST11, name=filename, 
        args=(filename, identity_virulence, identity_antimicrobial, coverage_virulence, coverage_antimicrobial, reads_type_value, sample_type_value))
    running_thread.start()
    
    return True,filename



def post_ST11(request):
    identity_virulence = str(request.POST.getlist('identity_virulence'))
    identity_virulence = identity_virulence.split('\'')
    identity_virulence = identity_virulence[1].split('%')
    identity_virulence = float(identity_virulence[0]) / 100
    #print(identity_virulence)
    identity_antimicrobial = str(request.POST.getlist('identity_antimicrobial'))
    identity_antimicrobial = identity_antimicrobial.split('\'')
    identity_antimicrobial = identity_antimicrobial[1].split('%')
    identity_antimicrobial = float(identity_antimicrobial[0]) / 100
    #print(identity_antimicrobial)
    coverage_virulence = str(request.POST.getlist('coverage_virulence'))
    coverage_virulence = coverage_virulence.split('\'')
    coverage_virulence = coverage_virulence[1].split('%')
    coverage_virulence = float(coverage_virulence[0]) / 100
    #print(coverage_virulence)
    coverage_antimicrobial = str(request.POST.getlist('coverage_antimicrobial'))
    coverage_antimicrobial = coverage_antimicrobial.split('\'')
    coverage_antimicrobial = coverage_antimicrobial[1].split('%')
    coverage_antimicrobial = float(coverage_antimicrobial[0]) / 100
    #print(coverage_antimicrobial)
    reads_type = str(request.POST.getlist('reads_type'))
    #print(reads_type)
    reads_type = reads_type.split('[\'')
    reads_type = reads_type[1].split('\']')
    #print(reads_type)
    reads_type = reads_type[0]
    #print(reads_type)
    if reads_type == 'Assembled or Draft Genome/Contigs':
        reads_type_value = 0
    else:
        reads_type_value = 1
    #print(reads_type_value)

    sample_type = str(request.POST.getlist('sample_type'))
    sample_type = sample_type.split('\'')
    sample_type = sample_type[1]
    if sample_type == 'mNGS_TGS':
        sample_type_value = 0
    elif sample_type == 'culture_TGS':
        sample_type_value = 1
    else:
        sample_type_value = 2 #culture_NGS
    #print(sample_type_value)

    country_value = str(request.POST.getlist('country_value'))
    country_value = country_value.split('\'')
    country_value = country_value[1]
    #print(country_value)
    email_value = str(request.POST.getlist('email'))
    email_value = email_value.split('\'')
    email_value = email_value[1]
    #print(email_value)
    save_data_value = str(request.POST.getlist('save_data_value'))
    save_data_value = save_data_value.split('\'')
    save_data_value = save_data_value[1]
    #print(save_data_value)

    file = request.FILES.getlist('file')

    i = 1
    if len(file) > 0:
        for file_i in file:

            checknamevalue,filename = handle_uploaded_file_ST11(file_i,i,save_data_value,country_value,email_value,
                                identity_virulence, identity_antimicrobial, coverage_virulence, coverage_antimicrobial, reads_type_value, sample_type_value) 
            if checknamevalue==False:
                return HttpResponse("Wrong_file_name")
            i = i + 1
        return HttpResponse(filename)
    else:
        return HttpResponse("No_file")
