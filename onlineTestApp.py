import web

render = web.template.render('views/')
db = web.database(dbn='postgres', user='dbuser1', pw='dbuser1', db='en2ardb')

urls = (
    '/', 'index',
    '/add','add',
    '/qaitems','qaitems', 
    '/search','search' 
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
        todos = db.query('select * from qaitems order by id desc limit 10')
        return render.qaitems(todos)

class add:
    def POST(self):
        i = web.input()
        n = db.insert('qaitems',question=i.question,answer=i.answer,tags=i.tags)
        raise web.seeother('/qaitems')
            


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

