from bs4 import BeautifulSoup
import sys
import os
import re

try:
 f = open(sys.argv[1],'r+')
 page = f.read()
except:
  print 'page not found ' + sys.argv[1] + "\n"
  exit(1)

soup=BeautifulSoup(page , 'html.parser')
table = soup.find("table",{"class": "u1"})

myDict = [] 

trList = table.findAll('tr')
for i,tr in enumerate(trList):
   if i == 0 or i == 1:
      continue
   tdL = tr.findAll('td')
   if tdL[1].text.find('U+06') != -1:
     myDict.append( tdL[1].text.replace('U+','')+":"+ tdL[3].text)

print myDict
