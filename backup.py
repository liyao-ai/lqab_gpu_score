#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

import os
import shutil
import time

path_self =""
path_main = os.path.abspath('')
path_main = path_main.replace(path_self,"")
#print (path_main)
path_source = path_main  + "\\data\\cnn_bilstm"# 备份数据文件路径
path = path_main + "\\data\\backup\\" + time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(time.time())) + "\\cnn_bilstm"  # 数据文件路径

print ("历史数据文件路径：",path_source)
print ("备份数据文件路径：",path)

if os.path.exists(path_source):  # 如果文件存在
    
    shutil.copytree(path_source,path) # 复制文件夹
    
else:
    print('no such file:%s'%path)  # 则返回文件不存在