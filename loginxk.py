# -*- coding:utf-8 -*-

import requests
import re
import urllib
from lxml import etree

# reload(sys)
# sys.setdefaultencoding('utf8')

def getVerifyCode(img):
    verifyCode = input("Enter the verify code: ")
    return verifyCode

def parseExamHTML(examHTML):
    root = etree.HTML(examHTML)
    tableRowsXPATH = "//tr"
    tableRows = root.xpath(tableRowsXPATH)
    res = []
    for index, row in enumerate(tableRows):
        if index == 0:
            continue
        tdXPath = 'td'
        tds = row.xpath(tdXPath)
        tdtexts = list(map(lambda x: x.text, tds))
        if tdtexts[3].isspace():
            continue
        # print ' '.join(tdtexts)
        res.append(' '.join(tdtexts))
    return '\n'.join(res)


def loginXK():
    header = {
        "Host": "xk.suda.edu.cn",
        "Connection": "keep - alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
    }
    loginURL = "http://xk.suda.edu.cn/default_szdx.aspx"

    checkCodeImgURL = "http://xk.suda.edu.cn/CheckCode.aspx"
    rs = requests.session()
    loginPageHTML = rs.get(url=loginURL, headers=header).content
    loginPageHTML = loginPageHTML.decode('gbk')
    vsDicRe = r'<input type="hidden" name="(.*?)" value="(.*?)"'
    temp = re.findall(vsDicRe, loginPageHTML)
    vsDic = dict(re.findall(vsDicRe, loginPageHTML))
    viewState = vsDic["__VIEWSTATE"]

    checkCodeImg = rs.get(checkCodeImgURL).content
    with open("checkCode.jpg", 'wb') as f:
        f.write(checkCodeImg)
    verifyCode = getVerifyCode(checkCodeImg)

    studentId = "1427407028"
    pwd = "znh706."

    postdata = {
        "__VIEWSTATE": viewState,
        "TextBox1": studentId,
        "TextBox2": pwd,
        "TextBox3": verifyCode,
        "Button1": ""
    }

    loginContent = rs.post(url=loginURL, data=postdata).content
    loginContent = loginContent.decode('gbk')
    with open("result.html", 'w', encoding='utf-8') as f:
        f.write(loginContent)

    loginResRe = r"<script language='javascript' defer>alert\('(.*?)'\)"

    loginResult = re.findall(loginResRe, loginContent)
    if len(loginResult) == 0:
        print("Login Success")
    else:
        # loginResult = loginResult[0].decode('gbk').encode('utf-8')
        print(loginResult)
        print("Please login again")
        loginXK()

    examTimeURLDic = {
        "xh": studentId,
        "xm": "%D7%F3%B3%BD%BA%C0",
        "gnmkdm": "N121610"
    }
    examTimeURLPar = urllib.parse.urlencode(examTimeURLDic)
    examTimeURL = "http://xk.suda.edu.cn/xskscx.aspx?" + examTimeURLPar

    header["Referer"] = "http://xk.suda.edu.cn/xs_main.aspx?xh=" + studentId
    examTimeRes = rs.get(url=examTimeURL, headers=header).content
    examTimeRes = examTimeRes.decode('gbk')
    with open("examRes.html", 'w', encoding='utf-8') as f:
        f.write(examTimeRes)

    examTimeText = parseExamHTML(examTimeRes)

    print(examTimeText)

def loginSession():
    header = {
        "Host": "xk.suda.edu.cn",
        "Connection": "keep - alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
    }
    loginURL = "http://xk.suda.edu.cn/default_szdx.aspx"

    checkCodeImgURL = "http://xk.suda.edu.cn/CheckCode.aspx"
    rs = requests.session()
    loginPageHTML = rs.get(url=loginURL, headers=header).content

    vsDicRe = r'<input type="hidden" name="(.*?)" value="(.*?)"'
    vsDic = dict(re.findall(vsDicRe, loginPageHTML))
    viewState = vsDic["__VIEWSTATE"]

    checkCodeImg = rs.get(checkCodeImgURL).content
    return rs, viewState, checkCodeImg


loginXK()