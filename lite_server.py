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
        data = data.decode('utf-8')
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
                res = user_dict[sid].login(vc)
                if(res==True):
                    return json.dumps(
                            {
                                'is_valid':1,
                                'data':user_dict[sid].getExamInfos()
                            })
                    #return user_dict[sid].getExamInfos()
                else:
                    return json.dumps(
                            {
                                'is_valid':0,
                                'data':res
                            })
                    #return res

if __name__ == "__main__":
    app.run()
