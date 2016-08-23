from bs4 import BeautifulSoup
import sys
import os
import urllib
import urllib2


a2b = {u'\u0621':"'", u'\u0623':'>', u'\u0624':'&', u'\u0625':'<', u'\u0626':'}', u'\u0627':'A', u'\u0628':'b', u'\u0629':'p', u'\u062A':'t', u'\u062B':'v', u'\u062C':'j', u'\u062D':'H', u'\u062E':'x', u'\u062F':'d', u'\u0630':'*', u'\u0631':'r', u'\u0632':'z', u'\u0633':'s', u'\u0634':'$', u'\u0635':'S', u'\u0636':'D', u'\u0637':'T', u'\u0638':'Z', u'\u0639':'E', u'\u063A':'g', u'\u0640':'_', u'\u0641':'f', u'\u0642':'q', u'\u0643':'k', u'\u0644':'l', u'\u0645':'m', u'\u0646':'n', u'\u0647':'h', u'\u0648':'w', u'\u0649':'Y', u'\u064A':'y', u'\u064B':'F', u'\u064C':'N', u'\u064D':'K', u'\u064E':'a', u'\u064F':'u', u'\u0650':'i', u'\u0651':'~', u'\u0652':'o', u'\u0653':'^', u'\u0654':'#', u'\u0670':'`', u'\u0671':'{', u'\u06DC':':', u'\u06DF':'@', u'\u06E0':'"', u'\u06E2':'[', u'\u06E3':';', u'\u06E5':',', u'\u06E6':'.', u'\u06E8':'!', u'\u06EA':'-', u'\u06EB':'+', u'\u06EC':'%', u'\u06ED':']'}

def get_bulkwater(word):
   return ''.join([a2b[x] for x in word.decode('utf-8')])

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
   return morpholgy_list 
   
get_morphology('wbktbhm')


