#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

import os
import shutil

path_self =""
path_main = os.path.abspath('')
path_main = path_main.replace(path_self,"")
#print (path_main)
path_source = path_main + "\\data\\backup\\00\\cnn_bilstm" # 备份数据文件路径
path = path_main  + "\\data\\cnn_bilstm" # 数据文件路径

print ("备份数据文件路径：",path_source)
print ("历史数据文件路径：",path)

def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path,i)  # 取文件绝对路径
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)

if os.path.exists(path):  # 如果文件存在
    
    del_file(path) #删除文件夹下所有文件
    shutil.rmtree(path) # 删除文件夹
    shutil.copytree(path_source,path) # 复制文件夹
    
else:
    print('no such file:%s'%path)  # 则返回文件不存在