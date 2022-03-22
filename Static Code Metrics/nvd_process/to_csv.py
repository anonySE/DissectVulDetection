import os
import csv

if __name__ == '__main__':
    headers = ['Path','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','Label']
    dirpath = os.getcwd()
    inpath = os.path.join(dirpath, "out.txt")
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
            Label = 0
            if (str.find("_VULN_") > 0) or (str.find("_OLD.c") > 0) :
                Label = 1
            elif (str.find("_PATCHED_") > 0)  or (str.find("_NEW.c") > 0) :
                Label = 0
            else :
                pos = pos + 16
                continue
            csvrow.append(lines[pos])
            for i in range(1, 16) :
                csvrow.append(lines[pos + i].partition(': ')[2])
            csvrow.append(Label)
            writer.writerow(csvrow)
            pos = pos + 16