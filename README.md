# cninfo
retrieve data from cninfo.

The cninfo has no robots.txt and the codes are only used for education research in university.

If you want to parse the code into exe file. please use the below coding in cmd.

"pyinstaller --onefile main.py -i cninfo.ico"

After successful parsing, two ways to run the exe.

1. user should use the below cmd line to run the exe. For example,

"main.exe -keyword 减持 预披露 -startdate 2019-01-01 -enddate 2019-05-15 -isfulltext false -tablename cninfo_test"

2. user can click the exe ico and input the information as requested.

Regarding Chinese input problem, please input 'chcp936' in the cmd windows every time when you want to use the cmd method to run the program.

It has a shortcoming that the data in the website are not guaranteed to be completely stored into the database.

To reduce or overcome the shortcoming in the website, you can update the cookies in the json file. To find the cookies in the cninfo website, users can use the Developer Tools in browser. firstly, Press F12 to open the Developer Tools and select Network tab, and then input the keyword in cninfo website search box and search more than twice to get a stable cookie. Second, find latest http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=**** in Developer Tools Network tab and get the cookie and input the cookie in json file accordingly. The cookie in Developer Tools is shown in the picture. 
