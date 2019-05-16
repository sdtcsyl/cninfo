# -*- coding: utf-8 -*-
"""
Created on May 15 2019

"""

import urllib

class cninfo:
    def __init__(self):
        self.url_index = 'http://www.cninfo.com.cn/new/index'
        self.url_search = 'http://www.cninfo.com.cn/new/fulltextSearch/full?'
        self.url_pdf = 'http://static.cninfo.com.cn/'
        
        
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
        
    def cninfo_search_cookie(self, keyword, sessionid): 
        cookie = {
                'JSESSIONID' : sessionid,
                'noticeTabClicks' : '%7B%22szse%22%3A3%2C%22sse%22%3A0%2C%22hot%22%3A0%2C%22myNotice%22%3A0%7D',
                'tradeTabClicks' : '%7B%22financing%20%22%3A0%2C%22restricted%20%22%3A0%2C%22blocktrade%22%3A0%2C%22myMarket%22%3A0%2C%22financing%22%3A2%7D', 
                'JSESSIONID' : sessionid,
                '_sp_ses.2141' : '*',
                'insert_cookie' : '45380249',
                'cninfo_search_record_cookie'  : keyword,
                '_sp_id.2141' : '77994138-513b-4934-ad4e-e34e19c6ec58.1557832115.1.1557832843.1557832115.d2fa6cc6-2fcd-418e-afc4-2ebe11b019ec'
                }
        return cookie
    
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
    
