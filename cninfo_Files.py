# -*- coding: utf-8 -*-
"""
Created on May 15 2019
"""

import os
#import sys


filepath = os.getcwd()
#return the 'scripts' folder path
parpath = filepath #os.path.dirname(filepath)
#return the parent folder of the 'scripts' folder


def createfolder(folder_path):
    directory = folder_path
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


db_path = createfolder(parpath + '\\Data\\DB') + '\\'
html_path = createfolder(parpath + '\\Data\\PDF') + '\\'
files_path = parpath+'\\' #createfolder(parpath + '\\Files') + '\\'
js_path = createfolder(parpath + '\\Data\\Json') + '\\'
log_path = createfolder('C:\\Users\\Public\\Documents\\cninfo\\Logging') + '\\cninfo_log.txt'
log_path1 = createfolder(parpath + '\\Data\\logging') + '\\cninfo_log.txt'

def writetxt(txt):
    
    txt_writer=open(log_path,'a')  #append
    txt_writer.writelines(txt)
    txt_writer.close()
    
    txt_writer=open(log_path1,'a')  #append
    txt_writer.writelines(txt)
    txt_writer.close()