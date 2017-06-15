import web
import json
from xkLogin import XKLogin

urls = (
    '/login','login'
)
app = web.application(urls, globals())
user_dict = dict()
class login:
    
    def GET(self):
        i = web.input()
        if('password' in i and 'sid' in i):
            print(i['sid'],i['password'])
    def POST(self):
        data = web.data()
        try:
            data = json.loads(data)
            if('pwd' in data):
                sid = data['sid'].replace('\n','')
                passwd = data['pwd'].replace('\n','')
                session = XKLogin(sid,passwd)
                user_dict[sid] = session
                return session.getCaptcha()
            elif('vc' in data):
                sid = data['sid'].replace('\n','')
                vc = data['vc'].replace('\n','')
                if(sid in user_dict):
                    return user_dict[sid].getExamInfos(vc)

        except:
            print("Login Failed,Got:[\n%s\n]" % str(data))



if __name__ == "__main__":
    app.run()
