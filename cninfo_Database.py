# -*- coding: utf-8 -*-
"""
Created on May 15 2019

@author: Yulu SU
"""

import sqlite3
import cninfo_Files as Files

def sqlwrite(data, table):    
    conn = sqlite3.connect(Files.db_path + 'cninfo.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''create table if not exists table_''' + 
                       table + 
                       '''(
                       id varchar(5),
                       secCode varchar(5),
                       secName varchar(5),
                       orgId varchar(5),
                       announcementId varchar(5),
                       announcementTitle varchar(5),
                       timestampStr varchar(5),
                       adjunctUrl varchar(5)  primary key,
                       adjunctSize varchar(5),
                       adjunctType varchar(5),
                       announcementType varchar(5),
                       announcementTypeName varchar(5),
                       associateAnnouncement varchar(5),
                       batchNum varchar(5),
                       columnId varchar(5),
                       sid varchar(5),
                       important varchar(5),
                       orgName varchar(5),
                       pageColumn varchar(5),
                       storageTime varchar(5),
                       page varchar(2),
                       NY varchar(2)
                       )''') 
        cursor.execute('''insert into table_''' + 
                       table + 
                       '''( id,
                       secCode,
                       secName,
                       orgId,
                       announcementId,
                       announcementTitle,
                       timestampStr,
                       adjunctUrl,
                       adjunctSize,
                       adjunctType,
                       announcementType,
                       announcementTypeName,
                       associateAnnouncement,
                       batchNum,
                       columnId,
                       sid,
                       important,
                       orgName,
                       pageColumn,
                       storageTime,
                       page,
                       NY
                       ) 
                       values (?,?,?,?,?,  ?,?,?,?,?,  ?,?,?,?,?, ?,?,?,?,?, ?,?)''', 
                       (data))
    except sqlite3.IntegrityError:
        pass
    cursor.rowcount
    cursor.close()
    conn.commit()
    conn.close()

def sqlselect(table, **args):    
    conn = sqlite3.connect(Files.db_path + 'cninfo.db')
    cursor = conn.cursor()
    cursor.execute('''create table if not exists table_''' + 
                       table + 
                       '''(
                       id varchar(5),
                       secCode varchar(5),
                       secName varchar(5),
                       orgId varchar(5),
                       announcementId varchar(5),
                       announcementTitle varchar(5),
                       timestampStr varchar(5),
                       adjunctUrl varchar(5)  primary key,
                       adjunctSize varchar(5),
                       adjunctType varchar(5),
                       announcementType varchar(5),
                       announcementTypeName varchar(5),
                       associateAnnouncement varchar(5),
                       batchNum varchar(5),
                       columnId varchar(5),
                       sid varchar(5),
                       important varchar(5),
                       orgName varchar(5),
                       pageColumn varchar(5),
                       storageTime varchar(5),
                       page varchar(2),
                       NY varchar(2)
                       )''') 
    
    if 'alldata' in args:
        cursor.execute('SELECT id  FROM table_' + table)  
    else:   
        cursor.execute('SELECT id, adjunctUrl, adjunctType FROM table_' + table + ' WHERE NY = 0') 
    res =cursor.fetchall()
    suc = res
    cursor.close()
    conn.commit()
    conn.close() 
    return suc
    

def sqlupdate(count, dl, table, record):    
    conn = sqlite3.connect(Files.db_path + 'cninfo.db')
    cursor = conn.cursor()     
    cursor.execute('UPDATE table_' + table + ' SET NY = ?  WHERE adjunctUrl = ?',(count, dl,)) 
    cursor.close()
    conn.commit()
    conn.close() 

def sqlcheck(table, **kws):
    conn = sqlite3.connect(Files.db_path + 'cninfo.db')
    cursor = conn.cursor()
    cursor.execute('''create table if not exists table_''' + 
                           table + 
                           '''(
                           id varchar(5),
                           secCode varchar(5),
                           secName varchar(5),
                           orgId varchar(5),
                           announcementId varchar(5),
                           announcementTitle varchar(5),
                           timestampStr varchar(5),
                           adjunctUrl varchar(5)  primary key,
                           adjunctSize varchar(5),
                           adjunctType varchar(5),
                           announcementType varchar(5),
                           announcementTypeName varchar(5),
                           associateAnnouncement varchar(5),
                           batchNum varchar(5),
                           columnId varchar(5),
                           sid varchar(5),
                           important varchar(5),
                           orgName varchar(5),
                           pageColumn varchar(5),
                           storageTime varchar(5),
                           page varchar(2),
                           NY varchar(2)
                           )''') 
    if 'filename' in kws:
        cursor.execute('SELECT id FROM table_' + table + ' WHERE id = ?',(kws['filename'],))
    if 'fileweb' in kws:
        cursor.execute('SELECT adjunctUrl FROM table_' + table + ' WHERE adjunctUrl = ?',(kws['fileweb'],))
    res =cursor.fetchall()
    suc = 0
    if len(res) > 0:
        suc = 1
    else:
        suc = 0 
    cursor.close()
    conn.commit()
    conn.close() 
    return suc

def sqloutput(table):
    conn = sqlite3.connect(Files.db_path + 'cninfo.db')
    cursor = conn.cursor()
    cursor.execute('select id, secCode, secName, announcementTitle, timestampStr, adjunctUrl, adjunctType, page from table_'+table)
    res =cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return res
    
