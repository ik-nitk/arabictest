import web
from bs4 import BeautifulSoup
import re
import base64
import sys
import json
import os
import urllib
import urllib2

render = web.template.render('views/')
db = 0

reg_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)





def dburl2dict(url):
    dbn, rest = url.split('://', 1)
    user, rest = rest.split(':', 1)
    pw, rest = rest.split('@', 1)
    host, rest = rest.split(':', 1)
    port, rest = rest.split('/', 1)
    db = rest
    return dict(dbn=dbn, user=user, pw=pw, db=db, host=host)


if len(sys.argv) > 1:
    herokudburl = os.environ.get('DATABASE_URL') 
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
    '/login' , 'Login', 
    '/randoml' , 'randomList', 
    '/morphology' , 'morphology' 
)

import model 

class mydict(dict):
     pass

def get_lex_morph(word):
   url = 'http://lexanalysis.com/cgi-bin/araflex.pl'
   values = {'queryOption':'queryByArabicWord',
             'queryToken': word,
             'submit':'submit'} 
   data = urllib.urlencode(values)
   req = urllib2.Request(url, data)
   response = urllib2.urlopen(req)
   page = response.read()
   soup=BeautifulSoup(page , 'html.parser')
   t = soup.find("table")
   tr = t.findAll('tr')
   morpholgy_list = []
   for r in tr[1:]: 
      morpholgy_list.append(str(r))
   return morpholgy_list[0] if len(morpholgy_list) else "" 

class morphology:
    def GET(self):
        querystr = ''
        inp = web.input()
        morph = []
        print inp
        if hasattr(inp,"txt") and inp.txt[0] < u'~':
            #english or other landuage is not supported 
            return json.dumps(morph)
        else:
            p = model.get_morphology(inp.txt)
            if bool(p) == False:
                p = []
                x = mydict
                x.root  = ''
                x.meaning = ''
                x.morphology1 = get_lex_morph(model.get_bulkwater(inp.txt))
                x.morphology2 = ''
                x.example = ''
                p.append(x)
            #json format
            if hasattr(inp,"json"):
               web.header('Content-Type', 'application/json')
               web.header('Access-Control-Allow-Origin', '*')
               web.header('Access-Control-Allow-Credentials', 'true')
               for i in p:
                    d = {'word':inp.txt,'morphology1':i.morphology1,'morphology2':i.morphology2,'meaning':i.meaning,'root':model.get_arabFrombulk(i.root),'example':i.example.encode('utf-8')};
                    morph.append(d)
                   #arrange in expected format
               return json.dumps(morph)
            else:
               for i in p:
                   i.root = model.get_arabFrombulk(i.root)
               return render.morphology(p,inp.txt)

def isMobile():
    if web.ctx.env.has_key('HTTP_USER_AGENT'):
        user_agent = web.ctx.env['HTTP_USER_AGENT']
        b = reg_b.search(user_agent)
        v = reg_v.search(user_agent[0:4])
        if b or v:
            return True 
    return False    

class index:
    def GET(self):
        return render.index()

class test:
    def GET(self):
        querystr = ''
        txt = '' 
        i = web.input()
        if hasattr(i,"txt"):
            txt = i.txt
            querystr = 'select * from qaitems where tags like \'%' + str(i.txt) + '%\' order by random() limit 15'
        else:
            querystr = 'select * from qaitems order by random() limit 15'
        todos = db.query(querystr); 
        return render.test(todos,txt,ismobile=isMobile())


class randomList:
    def GET(self):
        querystr = ''
        txt = '' 
        i = web.input()
        n = 20
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        if hasattr(i,"n"):
            n = int(i.n)
        if hasattr(i,"txt"):
            txt = i.txt
            querystr = 'select * from qaitems where tags like \'%' + str(i.txt) + '%\' order by random() limit ' + str(n)
        else:
            querystr = 'select * from qaitems order by random() limit ' + str(n)
        todos = db.query(querystr);
        qalist = [{'q': todo.question , 'a': todo.answer} for todo in todos]
        return json.dumps(qalist) 


class search:
    def GET(self):
        querystr = ''
        i = web.input()
        if hasattr(i,"value") and i.value is "morphology" :
            return morphology.GET(self)
        if hasattr(i,"txt") and i.txt[0] < u'~':
            #english  
            querystr = 'select * from qaitems where upper(answer) like \'%' + i.txt.upper() + '%\''
        else:
            querystr = 'select * from qaitems where question like \'%' + i.txt + '%\''
        todos = db.query(querystr);
        if len(todos):   
            return render.searchitems(todos)
        else:
            return "Not found !!!"

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
	print i 
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

