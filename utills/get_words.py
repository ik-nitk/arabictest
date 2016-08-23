from bs4 import BeautifulSoup
import sys
import os
import urllib
import urllib2
import sqlite3

reload(sys)
sys.setdefaultencoding("utf-8")

conn = sqlite3.connect('qdb')


a2b = {u'\u0621':"'",u'\u0622':"|", u'\u0623':'>', u'\u0624':'&', u'\u0625':'<', u'\u0626':'}', u'\u0627':'A', u'\u0628':'b', u'\u0629':'p', u'\u062A':'t', u'\u062B':'v', u'\u062C':'j', u'\u062D':'H', u'\u062E':'x', u'\u062F':'d', u'\u0630':'*', u'\u0631':'r', u'\u0632':'z', u'\u0633':'s', u'\u0634':'$', u'\u0635':'S', u'\u0636':'D', u'\u0637':'T', u'\u0638':'Z', u'\u0639':'E', u'\u063A':'g', u'\u0640':'_', u'\u0641':'f', u'\u0642':'q', u'\u0643':'k', u'\u0644':'l', u'\u0645':'m', u'\u0646':'n', u'\u0647':'h', u'\u0648':'w', u'\u0649':'Y', u'\u064A':'y', u'\u064B':'F', u'\u064C':'N', u'\u064D':'K', u'\u064E':'a', u'\u064F':'u', u'\u0650':'i', u'\u0651':'~', u'\u0652':'o', u'\u0653':'^', u'\u0654':'#', u'\u0670':'`', u'\u0671':'{', u'\u06DC':':', u'\u06DF':'@', u'\u06E0':'"', u'\u06E2':'[', u'\u06E3':';', u'\u06E5':',', u'\u06E6':'.', u'\u06E8':'!', u'\u06EA':'-', u'\u06EB':'+', u'\u06EC':'%', u'\u06ED':']',u' ':' ',u'(':'(',u')':')',u'[':'[',u']':']'}

vowels = {u'\u064B':'F', u'\u064C':'N', u'\u064D':'K', u'\u064E':'a', u'\u064F':'u', u'\u0650':'i', u'\u0651':'~', u'\u0652':'o', u'\u0653':'^', u'\u0654':'#', u'\u0670':'`', u'\u0671':'{', u'\u06DC':':', u'\u06DF':'@', u'\u06E0':'"', u'\u06E2':'[', u'\u06E3':';', u'\u06E5':',', u'\u06E6':'.', u'\u06E8':'!', u'\u06EA':'-', u'\u06EB':'+', u'\u06EC':'%', u'\u06ED':']'}

b2a = {value:key for key, value in a2b.iteritems()}
rvowels = {value:key for key, value in vowels.iteritems()}

def get_bulkwater(word):
   return ''.join([a2b[x] for x in word.decode('utf-8')])

def remove_vowels(word):
   # remove the vowels from the word
   return ''.join([x for x in word if x not in rvowels])

try:
 f = open(sys.argv[1],'r+')
 page = f.read()
except:
  print 'page not found ' + sys.argv[1] + "\n"
  exit(1)

soup=BeautifulSoup(page , 'html.parser')
nv = soup.find("div",{"class": "navigationPane"})

root = nv.find('b')
#print root.text.encode('utf-8')
bwr =  get_bulkwater(root.text.encode('utf-8'))

#h4 = soup.findAll("h4",{"class": "dxe"})

#h4l = []
#for i in  h4:
#   h4l.append(i)


def get_morphology(word):
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


def get_morphology2(link):
   url = 'http://corpus.quran.com/'+link
   req = urllib2.Request(url)
   response = urllib2.urlopen(req)
   page = response.read()
   soup=BeautifulSoup(page , 'html.parser')
   t = soup.find('td',{'class': "morphologyCell"})
   return str(t) 
   

print "-------------------------------------------------------------"
print "word\t|root\t|form\t|meaning\t|example"
print "-------------------------------------------------------------"


def parse_table(idx,t):
   tr = t.findAll('tr')
   for r in tr:
      sql = 'insert into quran_dict(qid,root,qword,qword_nv,example,meaning,morphology1,morphology2) values (NULL,'.encode('utf-8')
      td = r.findAll('td',{'class': 'c2'})
      meaning =td[0].text.encode('utf-8')
      mor_link = td[0].find('a').get('href')
      td = r.findAll('td',{'class': 'c3'})
      example = td[0].text.encode('utf-8')
      word= td[0].span.text.encode('utf-8')
      #print word+"\t|" + get_bulkwater(word)
      #print bwr+"\t|"
      sql = sql + u'"' + bwr.replace(' ','') + u'",'
      sql = sql + u'"' + get_bulkwater(word) + u'",'
      sql = sql + u'"' + remove_vowels(get_bulkwater(word)) + u'",'
      #print h4l[idx].text.split('-')[0]
      #sql = sql + '"'+ h4l[idx].text.split('-')[0] + '",'
      #print "\t|"+ meaning
      #print "\t|"+example
      sql = sql + u"'" + example.encode('utf-8') + u"',"
      sql = sql + u"'" + meaning.encode('utf-8') + u"',"
      #print "\n",get_morphology(get_bulkwater(word))
      #print "\n",get_morphology2(mor_link)  
      sql = sql + u"'" + get_morphology(get_bulkwater(word)).encode('utf-8').replace("'","\'\'") + u"',"
      sql = sql + u"'" + get_morphology2(mor_link).encode('utf-8').replace("'","\'\'") + u"')"
      print 'adding to databse \n\n' #+ sql.encode('utf-8')
      conn.execute(sql) 
      conn.commit()
       

li = soup.findAll("table",{"class": "taf"}) 
for idx,t in  enumerate(li):
   parse_table(idx,t)

print "Records created successfully";
conn.close()
