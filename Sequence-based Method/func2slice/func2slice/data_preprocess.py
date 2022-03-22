## coding:utf-8

import pickle
import os

slice_path = '/opt/func2slice/slices'
label_path = '/opt/func2slice/label_source/'
folder_path = '/opt/func2slice/slice_label/'
count1=0
count2=0
for filename in os.listdir(slice_path):
    if filename.endswith('.txt') is False:
        continue
    filepath = os.path.join(slice_path,filename)
    f = open(filepath,'r')
    slicelists = f.read().split('------------------------------')
    f.close()
    labelpath = os.path.join(label_path,filename[:-4]+'_label.pkl')
    f = open(labelpath,'rb')
    labellists = pickle.load(f)
    f.close()

    if(len(labellists) != len(slicelists)-1):
        labellists = labellists[0]

    if slicelists[0] == '':
        del slicelists[0]
    if slicelists[-1] == '' or slicelists[-1] == '\n' or slicelists[-1] == '\r\n':
        del slicelists[-1]
    
    print filename,len(slicelists),len(labellists)
    print labellists

    file_path = os.path.join(folder_path,filename)
    f = open(file_path,'a+')
    index = -1
    for slicelist in slicelists:
        sentences = slicelist.split('\n')
        if sentences[0] == '\r' or sentences[0] == '':
            del sentences[0]
        if sentences == []:
            continue
        if sentences[-1] == '':
            del sentences[-1]
        if sentences[-1] == '\r':
            del sentences[-1]
        slicename = sentences[0]
        #print slicename
        label = labellists[slicename]
        
        # index += 1
        # sentences = slicelist.split('\n')
        # if sentences[0] == '\r' or sentences[0] == '':
        #     del sentences[0]
        # if sentences == []:
        #     continue
        # if sentences[-1] == '':
        #     del sentences[-1]
        # if sentences[-1] == '\r':
        #     del sentences[-1]
        # print index,labellists[index]
        # label = labellists[index]
        # labellist = labellists[index]
        # for labels in labellist:
        #     if labels==1:
        #         label = 1
        #     else:
        #         label = 0
        if label==1:
            count1 += 1
        else:
            count2 += 1
        for sentence in sentences:
            f.write(str(sentence)+'\n')
        f.write(str(label)+'\n')
        f.write('------------------------------'+'\n')
    f.close()

print "vul:",count1," non-vul:",count2
print('\success!')
