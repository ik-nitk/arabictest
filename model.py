import web

db = web.database(dbn='sqlite', db='qdb')
'''
<Storage {'qid': 3, 'morphology1': u'', 'morphology2': u'<td class="morphologyCell"><b class="segNavy">CONJ</b> \u2013 pre
fixed conjunction <i class="ab">wa</i> (and)<br/><b class="segSky">N</b> \u2013 accusative masculine indefinite noun</td>'
, 'qword': u'wa>ab~FA', 'meaning': u'and grass', 'qword_nv': u'w>bA', 'root': u'>bb', 'example': u' \u0648\u064e\u0641\u06
4e\u0627\u0643\u0650\u0647\u064e\u0629\u064b \u0648\u064e\u0623\u064e\u0628\u0651\u064b\u0627'}>
>>>

'''

a2b = {u'\u0621':"'",u'\u0622':"|", u'\u0623':'>', u'\u0624':'&', u'\u0625':'<', u'\u0626':'}', u'\u0627':'A', u'\u0628':'b', u'\u0629':'p', u'\u062A':'t', u'\u062B':'v', u'\u062C':'j', u'\u062D':'H', u'\u062E':'x', u'\u062F':'d', u'\u0630':'*', u'\u0631':'r', u'\u0632':'z', u'\u0633':'s', u'\u0634':'$', u'\u0635':'S', u'\u0636':'D', u'\u0637':'T', u'\u0638':'Z', u'\u0639':'E', u'\u063A':'g', u'\u0640':'_', u'\u0641':'f', u'\u0642':'q', u'\u0643':'k', u'\u0644':'l', u'\u0645':'m', u'\u0646':'n', u'\u0647':'h', u'\u0648':'w', u'\u0649':'Y', u'\u064A':'y', u'\u064B':'F', u'\u064C':'N', u'\u064D':'K', u'\u064E':'a', u'\u064F':'u', u'\u0650':'i', u'\u0651':'~', u'\u0652':'o', u'\u0653':'^', u'\u0654':'#', u'\u0670':'`', u'\u0671':'{', u'\u06DC':':', u'\u06DF':'@', u'\u06E0':'"', u'\u06E2':'[', u'\u06E3':';', u'\u06E5':',', u'\u06E6':'.', u'\u06E8':'!', u'\u06EA':'-', u'\u06EB':'+', u'\u06EC':'%', u'\u06ED':']',u' ':' ',u'(':'(',u')':')',u'[':'[',u']':']'}

b2a = {value:key for key, value in a2b.iteritems()}

junk = {u'\udbff':' ', u'\udc02':' '}

vowels = {u'\u064B':'F', u'\u064C':'N', u'\u064D':'K', u'\u064E':'a', u'\u064F':'u', u'\u0650':'i', u'\u0651':'~', u'\u0652':'o', u'\u0653':'^', u'\u0654':'#', u'\u0670':'`', u'\u0671':'{', u'\u06DC':':', u'\u06DF':'@', u'\u06E0':'"', u'\u06E2':'[', u'\u06E3':';', u'\u06E5':',', u'\u06E6':'.', u'\u06E8':'!', u'\u06EA':'-', u'\u06EB':'+', u'\u06EC':'%', u'\u06ED':']'}

rvowels = {value:key for key, value in vowels.iteritems()}

def get_bulkwater(word):
   return ''.join([a2b[x] for x in word])

def get_arabFrombulk(word):
   return ''.join([b2a[x] for x in word])

def remove_vowels(word):
   return ''.join([x for x in word if x not in rvowels])

def get_morphology(w):
    word=get_bulkwater(w) 
    r= db.select('quran_dict', where="qword='"+word+"'",order='random()',limit=1)
    if bool(r) == False:
       word=remove_vowels(word)
       r= db.select('quran_dict', where="qword_nv='"+word+"'",order='random()',limit=1)
    return r
