from bs4 import BeautifulSoup
import sys
import os

try:
 f = open(sys.argv[1],'r+')
 page = f.read()
except:
  print 'page not found ' + sys.argv[1] + "\n"
  exit(1)

soup=BeautifulSoup(page , 'html.parser')
select = soup.find("select",id="entryList")

for option in select:
   print 'http://corpus.quran.com/qurandictionary.jsp?q='+option['value']
