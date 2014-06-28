import web
import re
import base64


render = web.template.render('views/')
db = web.database(dbn='postgres', user='dbuser1', pw='dbuser1', db='en2ardb')

urls = (
    '/', 'index',
    '/add','add',
    '/qaitems','qaitems', 
    '/search','search',
    '/login' , 'Login' 
)

class index:
    def GET(self):
        return render.index()


class search:
    def GET(self):
        querystr = ''
        i = web.input()
        if len(i.txt) and i.txt[0] < u'~':
            #english  
            querystr = 'select * from qaitems where answer like \'%' + i.txt + '%\''
        else:
            querystr = 'select * from qaitems where question like \'%' + i.txt + '%\''
        todos = db.query(querystr); 
        return render.searchitems(todos)

class qaitems:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            todos = db.query('select * from qaitems order by id desc limit 10')
            return render.qaitems(todos)
        else:
            raise web.seeother('/login')

class add:
    def POST(self):
        i = web.input()
        n = db.insert('qaitems',question=i.question,answer=i.answer,tags=i.tags)
        raise web.seeother('/qaitems')

#poor auth. but just a temp fix
allowed = (
    ('arabic','english'),
    ('english','arabic')
)

            
class Login:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ','',auth)
            username,password = base64.decodestring(auth).split(':')
            if (username,password) in allowed:
                raise web.seeother('/qaitems')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate','Basic realm="Need login"')
            web.ctx.status = '401 Unauthorized'
            return


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

