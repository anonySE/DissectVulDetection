import os
import csv

# Remove all the files named "io.c"
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
            str = ''
            csvrow = []
            pos = pos + 1
            str = lines[pos]
            if (str.find("/io.c']") > 0) :
                pos = pos + 16
                continue
            pos = pos + 16
            csvrow.append(lines[pos - 16])
            for i in range(15, 0, -1) :
                csvrow.append(lines[pos - i].partition(': ')[2])

            ########################################################################
            # The purpose of this part is to make 'path' consistent with that in "SARD_testcaseinfo.txt"
            ########################################################################
            path = str.replace("[u'/opt/ReSySeVR/data", '.')
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

            flag = 0
            with open(findpath, encoding='utf-8') as file:
                filelines = file.readlines()
                for fileline in filelines:
                    tmp = fileline.partition(' ')[0]
                    if tmp == path :
                        flag = 1
                        break
            csvrow.append(flag)
            writer.writerow(csvrow)