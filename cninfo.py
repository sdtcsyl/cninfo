# -*- coding: utf-8 -*-
"""
Created on May 15 2019
"""

import urllib
import json
#import execjs

def load_dic( filename: str):
    with open(filename, "r") as f:
        dic = json.load(f)
        return dic

class cninfo:
    def __init__(self):
        self.url_index = 'http://www.cninfo.com.cn/new/index'
        self.url_search = 'http://www.cninfo.com.cn/new/fulltextSearch/full?'
        self.url_pdf = 'http://static.cninfo.com.cn/'
        self.func_cookies= '''
            var cookieName = "cninfo_search_record_cookie";
            /**
             * 获取指定cookie的值
             * @param cookieName
             * @returns
             */
            function getCookie(cookieName) {
            	var strCookie = document.cookie;
            	var arrCookie = strCookie.split("; ");
            	for (var i = 0; i < arrCookie.length; i++) {
            		var arr = arrCookie[i].split("=");
            		if (cookieName == arr[0]) {
            			return arr[1];
            		}
            	}
            	return "";
            }
            /**
             * 记录cookie
             * @param varData
             */
            function markCookie(varData) {
            	varData = $.trim(varData);
            	varData = encodeURI(varData);
            	//alert('varData:'+varData);
            	var cookieValue = getCookie(cookieName);
            	//alert('b:' + cookieValue);
            	if (cookieValue == '') {
            		cookieValue = varData;
            	} else {
            		// 去重
            		var temp = cookieValue.split('|');
            		cookieValue = varData;
            		// 最多存储20个
            		var var_length = 19;
            		if (temp.length < var_length) {
            			var_length = temp.length;
            		}
            		for (var i = 0; i < var_length; i++) {
            			if (temp[i] == varData) {
            				continue;
            			} else {
            				cookieValue += '|' + temp[i];
            			}
            		}
            	}
            	//alert('a:' + cookieValue);
            	var exp = new Date();
            	exp.setTime(exp.getTime() + 10 * 24 * 60 * 60 * 1000);	//设置过期时间为10天
            	document.cookie = cookieName + "=" + cookieValue + ";expires=" + exp.toGMTString() + ";path=/";
            }'''
        #self.cxt = execjs.compile(self.decrypt)
        
        
    def cninfo_search_header(self, keyword):
        header = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'www.cninfo.com.cn',
                'Referer': 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord='+keyword,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
                }
        return header
        
    def cninfo_search_cookie(self, keyword, sessionid=''): 
        self.cookies = load_dic('cookie.json')
        self.cookies['cninfo_search_record_cookie']=keyword
        if sessionid != '':
            self.cookies['JSESSIONID']=sessionid
        return self.cookies
    
    def cninfo_search_keyword(self, keyword):
        if keyword == None:
            print("Please input not Null Keyword. Please press 'ENTER' after input.")
            keyword = input()
        while keyword =='':
            print("Please input not NULL Keyword. Please press 'ENTER' after input.")
            keyword = input()
        keyword = {'keyword':keyword}
        keyword = urllib.parse.urlencode(keyword)
        keyword = keyword.replace('keyword=','')
        return keyword
    
    def cninfo_search_startdate(self):
        print("Please input a start date (YYYY-MM-DD) or not. Please press 'ENTER' after input.")
        keyword = input()
        return keyword
    
    def cninfo_search_enddate(self):
        print("Please input an end date (YYYY-MM-DD) or not. Please press 'ENTER' after input.")
        keyword = input()
        return keyword
    
    def cninfo_search_isfulltext(self):
        keyword = ''
        print("Please input 'true' of 'false' for isfulltext option. Please press 'ENTER' after input.")
        keyword = input()
        if keyword =='':
            keyword = 'false'
        return keyword
    
    def cninfo_search_url(self, keyword, sdate, edate, isfulltext, page):
        cninfo_search_paras = 'searchkey=' + keyword +' &sdate=' + sdate + '&edate=' + edate + '&isfulltext='+ isfulltext +'&sortName=nothing&sortType=desc&pageNum='+ str(page)        
        return self.url_search + cninfo_search_paras
    
    
        