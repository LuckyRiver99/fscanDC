import re
import os
from argparse import ArgumentParser

# sys读取参数
arg = ArgumentParser(description='Fscan_quchong')
arg.add_argument('-i', '--file', nargs='*',dest='file',help='Scan multiple targets given in a txt file',type=str)
arg.add_argument('-o', '--outfile', dest='outfile', help='the file save result',  default='result.txt',type=str)
result = arg.parse_args()
# 数据结构

SSH=[]
ftp=[]
redis=[]
mysql=[]
mssql=[]
oracle=[]
Memcached=[]
poc=[]
WebTitle=[]
InfoScan=[]
rdp=[]
MS17010=[]
DC=[]
dic_use={
    # 可利用信息梳理
    r".*SSH.*":SSH,
    r".*redis.*":redis,
    r".*mysql.*":mysql,
    r".*oracle.*":oracle,
    r".*mssql.*":mssql,
    r".*Memcached.*":Memcached,
    r".*ftp.*":ftp,
    r".*poc.*":poc,
    r".*DC.*":DC,
    r".*InfoScan.*":InfoScan,

    # 端口开放
    r":(\d?3389|33899.*)":rdp,
    r".*MS17-010.*":MS17010,
    r".*WebTitle.*":WebTitle
}
pattern=r"----------.*----------"

def getInfo():
    filetargets=[]
    # 读取指定txt，支持多个
    if result.file!=None:
        filetargets=result.file
    else:
     # 遍历当前文件夹 读取全部txt
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if filename.endswith('txt'):
                    filetargets.append(filename)
    print("作用范围："+str(filetargets))
    for filepath in filetargets:
        with open(filepath,'r',encoding='utf-8') as f:
            for line in f.readlines():
               for key in dic_use.keys():
                   if re.findall(key,line): # 正则匹配
                       if not re.findall(pattern,line): # 去重原结果文件
                           dic_use[key].append(line)
                   dic_use[key]=list(set(dic_use[key])) # 去重

def output():
    if result.outfile !=None:
        filename=result.outfile
    with open(filename,"a",encoding='utf-8') as file:
        #清空输出文件
        file.seek(0)
        file.truncate()
        for key in dic_use:
            if len(dic_use[key])!=0:
                if '3389' in key:
                    file.write("----------"+"疑似RDP"+"----------"+"\n")
                    file.write("\n")
                else:
                    # 写入数据
                    file.write("----------"+key[2:-2]+"----------"+"\n")
                    file.write("\n")
            for i in dic_use[key]:
                file.write(i)
            file.write("\n")
    print("结果已生成："+filename)
def main():
    getInfo()
    output()

if __name__ == '__main__':
    main()