import web
import re
import base64
import sys


render = web.template.render('views/')
db = 0

def dburl2dict(url):
    dbn, rest = url.split('://', 1)
    user, rest = rest.split(':', 1)
    pw, rest = rest.split('@', 1)
    host, rest = rest.split(':', 1)
    port, rest = rest.split('/', 1)
    db = rest
    return dict(dbn=dbn, user=user, pw=pw, db=db, host=host)


if len(sys.argv) > 1:
    herokudburl = 'postgres://qnunlyibgshzgq:ZeahOaJlroCMuFLsrEIIFfU97j@ec2-23-23-177-33.compute-1.amazonaws.com:5432/dbr9jkn9itng93'
    d = dburl2dict(herokudburl)
    db = web.database(dbn=d['dbn'],
                    db=d['db'],
                    user=d['user'],
                    pw=d['pw'],
                    host=d['host'],
                    ) 
else:
    db = web.database(dbn='postgres', user='dbuser1', pw='dbuser1', db='en2ardb')

urls = (
    '/', 'index',
    '/add','add',
    '/qaitems','qaitems', 
    '/search','search',
    '/test','test',
    '/login' , 'Login' 
)

class index:
    def GET(self):
        return render.index()

class test:
    def GET(self):
        querystr = ''
        i = web.input()
        #if len(i.txt) and i.txt[0] < u'~':
            #english  
        #    querystr = 'select * from qaitems where answer like \'%' + i.txt + '%\''
        #else:
        querystr = 'select * from qaitems order by random() limit 15'
        todos = db.query(querystr); 
        return render.test(todos)



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
        #fisrt check if entry exist
        querystr = 'select 1 from qaitems where answer = \'' + i.answer + '\' limit 1'
        t = db.query(querystr)
        if len(t):
           raise web.seeother('/qaitems')
        else: 
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
    #port = int(os.environ.get('PORT', 8080))
    # If called from the command line, it will start an HTTP server on the port named in the first command line argument, or, if there is no argument, on port 8080.
    app.run()

