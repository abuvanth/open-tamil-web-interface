import tamil
import codecs
import sys
import copy
import math
import re
# setup the paths
from opentamiltests import *
from tamil.utf8 import get_letters
from tamil import wordutils, utf8
from spell import Speller, LoadDictionary
from solthiruthi.datastore import TamilTrie, DTrie, Queue
from solthiruthi.Ezhimai import *
from solthiruthi.resources import DICTIONARY_DATA_FILES
from solthiruthi.data_parser import *
from solthiruthi.dictionary import *
from solthiruthi.datastore import DTrie
from transliterate import azhagi, jaffna, combinational, algorithm
from flask import Flask,request,json,Response,render_template
from ngram.Corpus import Corpus
from ngram import LetterModels
from ngram.LetterModels import *
from ngram.WordModels import *
from tamil.txt2unicode import *
import tamil.utf8 as utf8
app=Flask(__name__)
@app.route("/")
def index():
     return render_template('first.html')
@app.route("/translite")
def trans():
     return render_template('translite.html')
@app.route("/tsci")
def uni():
     return render_template('unicode.html')
@app.route("/keechu")
def keechu():
     return render_template('keechu.html')
@app.route("/spell")
def spl():
     return render_template('spell.html')
@app.route("/number")
def num():
     return render_template('number.html')
@app.route("/anagram")
def anag():
     return render_template('anagram.html')
@app.route("/unigram")
def unig():
     return render_template('unigram.html')
@app.route("/ngram")
def ngra():
     return render_template('ngram.html')
@app.route("/<num>")
def numstr(num):
    if num.find(".")==-1:
       num=int(num)
    else:
       num=float(num)
    out=tamil.numeral.num2tamilstr( num )
    data = { "result" : out}
    json_string = json.dumps(data,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
@app.route("/tsci/<tsci>")
def unicod(tsci):
    cod=request.args.get("cod")
    if cod =='t2u':
       out=tamil.tscii.convert_to_unicode(tsci)
    elif cod=='u2t':
         out=unicode2tscii(tsci)
    data = { "result" : out}
    json_string = json.dumps(data,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
@app.route("/keechu/<k1>")
def keech(k1):
    dic={}
    for idx,kk in enumerate(k1.split(' ')):
            idx_len = len( get_letters(kk) )
            #print('w# ',idx, idx_len )
            dic[idx]=idx_len
    json_string = json.dumps(dic,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
@app.route("/translite/<tan>")
def translite(tan):
    tamil_tx=algorithm.Iterative.transliterate(azhagi.Transliteration.table,tan)
    data = { "result" : tamil_tx}
    json_string = json.dumps(data,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
@app.route("/spell/<k1>")
def spell_check(k1):
    speller =  Speller(lang=u"TA",mode="web")
    notok,suggs = speller.check_word_and_suggest( k1 )
    json_string = json.dumps(suggs,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
@app.route("/ngram/<ng>")
def test_ngram(ng):
    obj = DTrie()
    prev_letter = u''
            # per-line processor - remove spaces
    for char in u"".join(re.split('\s+',ng)).lower():
        if prev_letter.isalpha() and char.isalpha():
           bigram = u"".join([prev_letter,char])
           obj.add(bigram)
                # update previous
        prev_letter = char
    actual = obj.getAllWordsAndCount()
    json_string = json.dumps(actual,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
@app.route("/anagram/<word>")
def anagram(word):
    AllTrueDictionary = wordutils.DictionaryWithPredicate(lambda x: True)
    TVU,TVU_size = DictionaryBuilder.create(TamilVU)
    length = len(utf8.get_letters(word))
    actual =list(wordutils.anagrams(word,TVU))
    json_string = json.dumps(actual,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
@app.route('/unigram/<word>')   
def test_basic(word):
        #WordModels
    n= request.args.get("n")
    print n
    t= get_ngram_groups( word, int(n))
    json_string = json.dumps(t,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
if __name__=="__main__":
   app.run(host='0.0.0.0',port=8080,debug=True)
