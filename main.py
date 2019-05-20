# -*- coding: utf-8 -*-
"""
Created on May 15 2019

@author: Yulu SU
"""
import cninfo
import cninfo_Database as DB
import cninfo_Files as File
import requests
from datetime import datetime
import time
import json
import pandas as pd
import argparse
import threading
from functools import wraps


#for step 1, get a table name for database
def func_input_tablename(keyword):
    while keyword == None or keyword == '':
        print("Please input a BLANK NEW Table Name in the database. Please press 'ENTER' after input.")
        keyword = input()
    nums = DB.sqlselect(keyword, alldata=1)
    while len(nums)>1:
        print("Please input a BLANK NEW Table Name in the database. Please press 'ENTER' after input.")
        keyword = input()
        nums = DB.sqlselect(keyword, alldata=1)
    return keyword

#for step 2, get data from the website and wait if Internet unstable
def func_request_data(url_full_search, header, cookie):
    try:
        req = requests.get(url_full_search, headers = header, cookies = cookie, timeout = 300)
    except requests.ConnectionError:    #if the internet is not steable
                internet = True
                while internet:
                    try:
                       time.sleep(600) #retry after timeout
                       req = requests.get(url_full_search, headers = header, cookies = cookie, timeout = 300)
                    except requests.ConnectionError:    #if the internet is not steable
                        pass
                    else:
                        internet =False
    finally:
            return req


#for step 2, clean the json data for database
def func_clean_data(announcement, isfulltext):
    #clean the announcementTitle
    announcementTitle = announcement['announcementTitle'].replace('<em>','')
    announcementTitle = announcementTitle .replace('</em>','')
    
    #adjust the timestamp from the website to the date
    dt_object = datetime.fromtimestamp(announcement['announcementTime']/1000)
    timestampStr = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    
    #generate the tuple for data
    data = (announcement['secCode'],announcement['secName'],announcement['orgId'],
            announcement['announcementId'],announcementTitle,timestampStr,
            announcement['adjunctUrl'],str(announcement['adjunctSize']),announcement['adjunctType'],
            announcement['announcementType'],announcement['announcementTypeName'],announcement['associateAnnouncement'],
            announcement['batchNum'],announcement['columnId'],announcement['id'],
            announcement['important'],announcement['orgName'],announcement['pageColumn'],
            announcement['storageTime'])
    
    #return a website url for a file from data
    fileweb = announcement['adjunctUrl']
    
    #return a file name from data
    if not isfulltext:
        filename = announcement['secCode']+'_'+announcement['secName']+'_'+ announcementTitle+ '_'+ timestampStr
    else:
        filename = announcementTitle+ '_'+ timestampStr
        
    if len(filename)>150:
        filename = filename[0:150]
    
    return data, fileweb, filename


#for step 3, return a revised file name for downloading the PDF file
def func_file_name(str_nm):
    str_nm = str_nm.replace('：','')
    str_nm = str_nm.replace(':','')
    str_nm = str_nm.replace('*','-')
    str_nm = str_nm.replace('/','')
    str_nm = str_nm.replace("\\",'')
    str_nm = str_nm.replace('?','')
    str_nm = str_nm.replace('<','')
    str_nm = str_nm.replace('>','')
    str_nm = str_nm.replace('|','')
    return str_nm


#for step 3, download the PDF file
def time_limit(interval):
    def deco(func):
        @wraps(func)
        def time_out():
            raise TimeoutError()
        
        def deco(*args, **kwargs):
            try:
                timer= threading.Timer(interval, time_out)
                timer.start()
                func(*args, **kwargs)
            except KeyboardInterrupt:
                print("Timeout reached!")
                timer.cancel()
                return -1
            finally:
                timer.cancel()
                return 1
        return deco
    return deco

@time_limit(300) #time out setting, if this part is over 2mins, the program will start next part    
def SaveAsPDF(str_nm, r):
     with open(str_nm, 'wb') as f:   
            f.write(r.content)      #write the data into a PDF 

def func_download_file(url, path):
    try:
        r = requests.get(url, stream=True, timeout = 600)
    except requests.ConnectionError:    #if the internet is not steable
        internet = True
        while internet:
            try:
               time.sleep(600) #retry after timeout
               r = requests.get(url, stream=True, timeout = 600)
            except requests.ConnectionError:    #if the internet is not steable
                pass
            else:
                internet =False
    try:
        SaveAsPDF(path, r)
        return True
    except TimeoutError:
        return False


if __name__ == '__main__':   
    
    #step 1, get the cninfo class and initiate it
    cninfo = cninfo.cninfo()
    
    url_index = cninfo.url_index
    url_search = cninfo.url_search
    url_pdf = cninfo.url_pdf    
    
    parser=argparse.ArgumentParser()
    parser.add_argument('-keyword', nargs='+', type=str, help='Please input not Null Keyword.')
    parser.add_argument('-startdate', default='', help='Please input a start date (YYYY-MM-DD).')
    parser.add_argument('-enddate', default='', help='Please input an end date (YYYY-MM-DD).')
    parser.add_argument('-isfulltext', default='false', help="Please input 'true' of 'false' for isfulltext option.")
    parser.add_argument('-tablename', default=False, help='Please input a new not null Table Name in the database')
    
    args = parser.parse_args()
    keyword = args.keyword
    if keyword != None:
        keyword = cninfo.cninfo_search_keyword('+'.join(keyword))
        sdate = args.startdate
        edate = args.enddate
        isfulltext = args.isfulltext
        tablename = args.tablename
        tablename = func_input_tablename(tablename)
    else:
        keyword = cninfo.cninfo_search_keyword(keyword)
        sdate = cninfo.cninfo_search_startdate()
        edate = cninfo.cninfo_search_enddate()
        isfulltext = cninfo.cninfo_search_isfulltext()
        tablename = func_input_tablename('')
    
    print('''\n\n****************************************\nkeyword = '''+ keyword + '''\n''' + 
          '''startdate = ''' + sdate +'''\n'''+ '''enddate = ''' + edate +'''\n'''+ '''isfulltext = ''' + isfulltext +'''\n'''+ '''tablename = ''' + tablename +'''\n\n****************************************\n'''+
          '''PROCEED or NOT [Y|N] \n''')
    proceed = input()
    
    if proceed == 'Y':    
        log = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' : keyword = ' + keyword + ', start date = ' +  sdate +', end date = '+edate + ', isfulltext = ' + isfulltext+ ', tablename = ' + tablename+'.\n'
        File.writetxt(log)
        
        #keyword = '%E5%87%8F%E6%8C%81+%E9%A2%84%E6%8A%AB%E9%9C%B2'
        sessionid = '004E026A14D6EC54C79B72D0C7CC9E22'
        
        header = cninfo.cninfo_search_header(keyword)
        cookie = cninfo.cninfo_search_cookie(keyword, sessionid)
        
        
        #step 2, retrieve the data from website and store the data into the database
        count = totalpages = totalannouncement = 1    
         
        for j in range(1,15):
            for i in range(1, totalpages+1, 1):             
                url_full_search = cninfo.cninfo_search_url(keyword, sdate, edate, isfulltext, i)            
                data_search = func_request_data(url_full_search, header, cookie)
                
                try: 
                    sessionid = data_search.cookies.get_dict()['JSESSIONID']
                    cookie = cninfo.cninfo_search_cookie(keyword, sessionid) 
                    json_search = data_search.json()
                    
                    if count == 1:
                        totalpages = json_search['totalpages']
                        totalannouncement = json_search['totalAnnouncement']                    
                        print('Step 1 has ' + str(totalpages) + ' pages and ' + str(totalannouncement) + ' announcements.')
                        count += 1
                        
                    announcements = json_search['announcements']
                    for announcement in announcements:
                        data, file_web, file_orig_name = func_clean_data(announcement, isfulltext)
                        num  = 0
                        file_full_name = file_orig_name
                        if(DB.sqlcheck(tablename, fileweb = file_web)!=1):
                            while(DB.sqlcheck(tablename, filename = file_full_name)):
                                num += 1
                                file_full_name = file_orig_name + '_[' + str(num) +']'
                            full_data = (file_full_name,) + data + (0,)
                            DB.sqlwrite(full_data, tablename) 
                except (json.JSONDecodeError, KeyError, AttributeError):
                    pass
              
            numbers = DB.sqlselect(tablename,alldata=1)
            if len(numbers) == totalannouncement:
                break
        
        print('Step 1 is done!')    
        print('The step 2 has collected ' + str(len(numbers)) + ' PDFs infomration . ')
        
        #step 3, retrieve the data from database and download the PDF files accordingly.
        for j in range(1,10):
            undownload_files = DB.sqlselect(tablename)
            for file in undownload_files:
                url = url_pdf + file[1]
                if file[2] == None:
                    str_nm = func_file_name(file[0])+'.html'
                else:
                    str_nm = func_file_name(file[0])+'.'+file[2].lower()
                path = File.createfolder(File.html_path + tablename) + '\\'+ str_nm
                if func_download_file(url, path):
                   DB.sqlupdate('1', file[1], tablename,'')
        
        
        #step 4, output control sheet
        output = DB.sqloutput(tablename)
        output_excel = pd.DataFrame(output,columns = ['ID', 'CompanyCode', 'CompanyName', 'announcementTitle', 'Date&Time', 'WebUrl', 'FileType'])
        output_excel.to_excel(File.db_path + tablename + '_ControlSheet.xlsx',index=False)
        
        print('Downloaded. Please check! ')
        time.sleep(10)
        