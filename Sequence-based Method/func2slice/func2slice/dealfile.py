## coding:utf-8
'''
##该程序用于获取nvd漏洞行
'''

import pickle
import os
import shutil

##处理nvd的函数文件，记录漏洞行    
def dealfunc_nvd_new(folder_path, diff_path):
	vulline_dict = {}  # 记录源程序中的漏洞行行号
	for cve_id in os.listdir(folder_path):
		for filename in os.listdir(os.path.join(folder_path, cve_id)):
			flag = 0
			for diffname in os.listdir(os.path.join(diff_path, cve_id)):
				if diffname[:-5] in filename:
					flag = 1
					break
			if flag == 0:   # 版本号对应不上，找不到对应的diff文件
				continue
			if 'NEW' in filename:              # NEW文件无漏洞
				continue

			filepath = os.path.join(folder_path, cve_id, filename)
			f = open(filepath, 'r')
			sentences = f.read().split('\n')   # 源文件func
			f.close()
			diffpath = os.path.join(diff_path,cve_id,diffname)
			f = open(diffpath, 'r')
			diffsens = f.read().split('\n')    # diff文件
			f.close()

			vul_code = []
			index = -1
			index_start = []
			for sen in diffsens:
				index += 1
				if sen.startswith('@@ ') is True:  # 记录diff文件中的@@行
					index_start.append(index)      # 记录@@段在diff文件中的行号
			for i in range(0, len(index_start)):   # 当前@@段
				if i < len(index_start) - 1:
					diff_sens = diffsens[index_start[i]:index_start[i + 1]]   # 该段@@段在diff文件中的行
				else:  # 最后一个@@段
					diff_sens = diffsens[index_start[i]:]
				startline = diff_sens[0]
				diff_sens = diff_sens[1:]  # diff段代码
				index = -1
				for sen in diff_sens:
					index += 1
					if sen.startswith('-') is True and sen.startswith('---') is False:  # 减号行
						if sen.strip('-').strip() == '' or sen.strip('-').strip() == ',' or sen.strip(
								'-').strip() == ';' or sen.strip('-').strip() == '{' or sen.strip('-').strip() == '}':
							continue
						vul_code.append(sen.strip('-').strip())

			for i in range(0, len(sentences)):
				if sentences[i].strip() not in vul_code:   # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
					continue
				else:
					linenum = i + 1
					if filepath.split('/')[-1] not in vulline_dict.keys():
						vulline_dict[filepath.split('/')[-1]] = [linenum]
					else:
						vulline_dict[filepath.split('/')[-1]].append(linenum)

	print vulline_dict
	with open('./vul_context_func.pkl','wb') as f:
		pickle.dump(vulline_dict,f)
	f.close()

                
                                
if __name__ == "__main__":
    
    data_source1 = '/opt/NVD/NVD_func/libpng/'
    diff_path = '/opt/NVD/NVD_diff/libpng/'
    dealfunc_nvd_new(data_source1,diff_path)

