import os
import csv

# Remove all the files named "io.c" and choose only those function slices with absolutely correct labels
if __name__ == '__main__':
    headers = ['Path','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','Label']
    dirpath = os.getcwd()
    inpath = os.path.join(dirpath, "out.txt")
    findpath = os.path.join(dirpath, "SARD_testcaseinfo.txt")
    outpath = os.path.join(dirpath, "data.csv")
    with open(inpath, encoding='utf-8') as f:
        lines = f.readlines()
    linelen = len(lines)
    pos = 0
    with open(outpath,'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        while pos < linelen :
            csvrow = []
            str1 = lines[pos]
            tmp = str1.find('{location:"')
            str1 = str1[tmp + 11:]
            tmp = str1.find(':')
            rownum = int(str1[:tmp])
            pos = pos + 1
            str2 = lines[pos]
            if (str2.find("/io.c']") > 0) :
                pos = pos + 16
                continue

            ########################################################################
            # The purpose of this part is to make 'path' consistent with that in "SARD_testcaseinfo.txt"
            ########################################################################
            path = str2.replace("[u'/opt/ReSySeVR/data", '.')
            path = path.replace("[u'/mnt/c/Users/Lyy/PycharmProjects/ReSySeVR/data", '.')
            path = path.replace("']\n", '')
            path = path.replace('/1/', '/')
            path = path.replace('/2/', '/')
            path = path.replace('/3/', '/')
            path = path.replace('/4/', '/')
            path = path.replace('/5/', '/')
            path = path.replace('/6/', '/')
            path = path.replace('/7/', '/')
            path = path.replace('/8/', '/')
            path = path.replace('/9/', '/')
            ########################################################################
            
            label = 0
            targetnum = 0
            with open(findpath, encoding='utf-8') as file:
                filelines = file.readlines()
                for fileline in filelines:
                    tmp = fileline.partition(' ')[0]
                    if tmp == path :
                        targetnum = int(fileline.partition(' ')[2])
                        label = 1
                        break
            csvrow.append(lines[pos])
            for i in range(1, 16) :
                csvrow.append(lines[pos + i].partition(': ')[2])
            if (label == 0) or (label == 1 and (targetnum == 0 or (rownum <= targetnum and ((pos + 17 > linelen) or (lines[pos] != lines[pos + 17]))))):
                csvrow.append(label)
            elif rownum > targetnum :
                pos = pos + 16
                continue
            elif rownum <= targetnum and lines[pos] == lines[pos + 17] :
                tmpstr = lines[pos + 16]
                tmp = tmpstr.find('{location:"')
                tmpstr = tmpstr[tmp + 11:]
                tmp = tmpstr.find(':')
                tmprownum = int(tmpstr[:tmp])
                if tmprownum <= targetnum :
                    csvrow.append(0)
                else :
                    csvrow.append(1)
            writer.writerow(csvrow)
            pos = pos + 16