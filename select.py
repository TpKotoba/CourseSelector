import requests
import os
from bs4 import BeautifulSoup

# LoginInfo
#
#     You must modify these every time you use this program.
#
# regno = Your student ID
# extid:
#    1. Sign-in the NTU selection system
#    2. Copy the extid from the url

regno = 'B07201027'
extid = '20210128015272d4d6c67fb0842ab16cc85f409b52dd'

def getPeople(_result, _index):
    try:
        peo = int(_result[_index].getText().strip())
        pass
    except:
        peo = -1
        pass
    return peo

def getProbability(_serno):
    url = 'https://if177.aca.ntu.edu.tw/coursetake/index.php/ctake/add-cou?regno=B07201027&extid=%s&code=2&sel_cou=0&opFld=serno&serno=%s&priority=1'%(extid, _serno)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    
    result = [i.getText().strip() for i in soup.find_all("td", class_="align-middle")]
    
    TotalSelect = int(result[12])
    if result[8] == '無限制(0)':
        HaveSelect = int(result[9])
        Limit = int(result[7])
        pass
    else:
        HaveSelect = int(result[10])
        Limit = int(result[8])
        pass
    return ((Limit-HaveSelect)/TotalSelect, result[4])

def compareProbability():
    _Courses = initCourses()
    rtn = {}
    s = sorted(_Courses, key = getProbability, reverse = True)
    for i in s:
        rtn[i] = getProbability(i)
    return rtn

def initCourses():
    Courses = []
    with open("courses.txt") as FILE:
        for LINE in FILE:
            Courses.append(LINE.strip())
            pass
        pass
    return Courses

def selectCourse(_serno, _prio):
    url1 = 'https://if177.aca.ntu.edu.tw/coursetake/index.php/ctake/add-cou?serno=%s&cougrp=&regno=B07201027&extid=%s&code=2&sure=確定選課&priority=%s'%(_serno, extid, _prio)
    page1 = requests.get(url1)
    return None

def selectCourses():
    cprC = compareProbability()
    i = 1
    for ser in cprC:
        selectCourse(ser, i)
        i += 1
        pass
    return i

if __name__ == '__main__':
    regno = input("輸入學號：")
    extid = input("輸入登錄資訊：")
    input("成功新%d個課程。按任一鍵結束.."%(selectCourses()-1))
