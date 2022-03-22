## coding:utf-8
import pickle
import os

def get_vulline(folder_path,_dict,label_path):

    for folder in os.listdir(folder_path):
        vulline_dict = {}
        for filename in os.listdir(os.path.join(folder_path,folder)):
            print(filename)
            filepath = os.path.join(folder_path,folder,filename)
            f = open(filepath,'r')
            slicelists = f.read().split('------------------------------')
            if slicelists[0] == '':
                del slicelists[0]
            if slicelists[-1] == '' or slicelists[-1] == '\n' or slicelists[-1] == '\r\n':
                del slicelists[-1]
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
                #SARD切片名
                if 'sard' in folder_path:
                    slicename = sentences[0].split(' ')[1].split('/')[-2] + '/' + sentences[0].split(' ')[1].split('/')[-1]
                    #slicename = sentences[0].split(' ')[1].split('/')[-4] + sentences[0].split(' ')[1].split('/')[-3] + sentences[0].split(' ')[1].split('/')[-2] + '/' + sentences[0].split(' ')[1].split('/')[-1]
                #NVD切片名
                elif 'nvd' in folder_path:
                    #slicename = sentences[0].split(' ')[1].split('/')[-3] + '/' + sentences[0].split(' ')[1].split('/')[-2] + '/' + sentences[0].split(' ')[1].split('/')[-1]
		    slicename = sentences[0].split(' ')[1]
                labelname = sentences[0].split(' ')[0] + '_' + sentences[0].split(' ')[1].split('/')[-1]

                #查找切片行行号
                sentences = sentences[1:]
                if slicename not in _dict.keys():
                    continue
                vullines = _dict[slicename]

                labellist = []
                for sentence in sentences:
                    if (is_number(sentence.split(' ')[-1])) is False:
                        continue
                    linenum = int(sentence.split(' ')[-1])
                    if linenum in vullines:
                        labellist.append(int(linenum))
                    else:
                        continue
                vulline_dict[labelname] = labellist
    
            with open(os.path.join(label_path,filename[:-4]+'_vulline.pkl'),'wb') as f:
                pickle.dump(vulline_dict,f)
            f.close()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

if __name__ == '__main__':

    data_path = '/opt/func2slice/nvdslices/nvd'
    vulline_path = '/opt/func2slice/vulline'
    if 'sard' in data_path:
        with open('./contain_all.txt','r') as f:
            vulline_lists = f.read().split('\n')
        f.close()

        _dict = {}
        for vulline_list in vulline_lists:
            name = vulline_list.split(' ')[0].split('/')[-4] + vulline_list.split(' ')[0].split('/')[-3] + vulline_list.split(' ')[0].split('/')[-2] + '/' + vulline_list.split(' ')[0].split('/')[-1]
            line = vulline_list.split(' ')[1]
            if name not in _dict.keys():
                _dict[name] = [line]
            else:
                _dict[name].append(line)
    elif 'nvd' in data_path:
        with open('/opt/func2slice/vul_context_func.pkl','rb') as f:
            _dict = pickle.load(f)
        f.close()
    get_vulline(data_path,_dict,vulline_path)
    
    
