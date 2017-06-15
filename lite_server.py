import web

urls = (
    '/login/','login'
)
app = web.application(urls, globals())

class login:
    def GET(self):
        i = web.input()
        if('password' in i and 'sid' in i):
            print i['sid'],i['password']



if __name__ == "__main__":
    app.run()