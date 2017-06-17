import tamil
import codecs
# setup the paths
from opentamiltests import *
from tamil.utf8 import get_letters
from spell import Speller, LoadDictionary
from transliterate import azhagi, jaffna, combinational, algorithm
from flask import Flask,request,json,Response,render_template
from ngram.Corpus import Corpus
from ngram import LetterModels
import tamil.utf8 as utf8
app=Flask(__name__)
@app.route("/")
def index():
     return render_template('index.html')
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
    out=tamil.tscii.convert_to_unicode(tsci)
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
if __name__=="__main__":
   app.run(host='0.0.0.0',port=8080,debug=True)

