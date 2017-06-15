import requests
import re
import urllib
from lxml import etree

LoginURL = "http://xk.suda.edu.cn/default_szdx.aspx"
CheckCodeImgURL = "http://xk.suda.edu.cn/CheckCode.aspx"

class XKLogin:
    def __init__(self, studentID, pwd):
        self.studentID = studentID
        self.pwd = pwd
        self.session = None
        self.viewState = None

    def getCaptcha(self):
        header = {
            "Host": "xk.suda.edu.cn",
            "Connection": "keep - alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
        }
        self.session = requests.session()
        loginPageHTML = self.session.get(url=LoginURL, headers=header).content
        loginPageHTML = loginPageHTML.decode('gbk')
        vsDicRe = r'<input type="hidden" name="(.*?)" value="(.*?)"'
        vsDic = dict(re.findall(vsDicRe, loginPageHTML))
        self.viewState = vsDic["__VIEWSTATE"]

        checkCodeImg = self.session.get(CheckCodeImgURL).content
        with open("checkCode.jpg", 'wb') as f:
            f.write(checkCodeImg)
        return checkCodeImg

    def login(self, verifyCode):
        header = {
            "Host": "xk.suda.edu.cn",
            "Connection": "keep - alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
        }
        postdata = {
            "__VIEWSTATE": self.viewState,
            "TextBox1": self.studentID,
            "TextBox2": self.pwd,
            "TextBox3": verifyCode,
            "Button1": ""
        }
        loginContent = self.session.post(url=LoginURL, data=postdata).content
        loginContent = loginContent.decode('gbk')

        loginResRe = r"alert\('(.*?)'\);</script>"
        loginResult = re.findall(loginResRe, loginContent)
        if len(loginResult) == 0:
            print("Login Success")
            return True
        else:
            # loginResult = loginResult[0].decode('gbk').encode('utf-8')
            print(loginResult)
            return loginResult[0]

    def getExamInfos(self):
        header = {
            "Host": "xk.suda.edu.cn",
            "Connection": "keep - alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
        }

        examTimeURLDic = {
            "xh": self.studentID,
            "xm": "%D7%F3%B3%BD%BA%C0",
            "gnmkdm": "N121610"
        }

        examTimeURLPar = urllib.parse.urlencode(examTimeURLDic)
        examTimeURL = "http://xk.suda.edu.cn/xskscx.aspx?" + examTimeURLPar

        header["Referer"] = "http://xk.suda.edu.cn/xs_main.aspx?xh=" + self.studentID
        examTimeRes = self.session.get(url=examTimeURL, headers=header).content
        examTimeRes = examTimeRes.decode('gbk')
        examTimeText = self.parseExamHTML(examTimeRes)
        return examTimeText

    def parseExamHTML(self, examHTML):
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


if __name__ == "__main__":
    l = XKLogin("1427407028", "znh706")
    l.getCaptcha()
    verifyCode =  input("Enter the verify code: ")
    l.login(verifyCode)
    res = l.getExamInfos()
    print(res)
