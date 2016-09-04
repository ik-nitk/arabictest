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
nv = soup.find("div",{"class": "sectionArea"})

for elem in nv:
   print 'http://corpus.quran.com/qurandictionary.jsp'+elem.get('href')
