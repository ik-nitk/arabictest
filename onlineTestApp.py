import web

render = web.template.render('views/')
db = web.database(dbn='postgres', user='dbuser1', pw='dbuser1', db='tempdb')

urls = (
    '/', 'index',
    '/add','add',
    '/qaitems','qaitems' 
)

class index:
    def GET(self):
        return render.index()


class qaitems:
    def GET(self):
        #todos = db.select('todo')
        todos = db.query('select * from todo order by id desc limit 10')
        return render.index(todos)

class add:
    def POST(self):
        i = web.input()
        n = db.insert('todo',question=i.question,answer=i.answer,tags=i.tags)
        raise web.seeother('/')
            


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

