import tamil
import codecs
# setup the paths
from opentamiltests import *
from tamil.utf8 import get_letters
from flask import Flask,request,json,Response
from ngram.Corpus import Corpus
from ngram import LetterModels
import tamil.utf8 as utf8
app=Flask(__name__)
@app.route("/")
def index():
     return "get request"
@app.route("/<k1>")
def unicod(k1):
    dic={}
    for idx,kk in enumerate(k1.split(' ')):
            idx_len = len( get_letters(kk) )
            #print('w# ',idx, idx_len )
            dic[idx]=idx_len
    json_string = json.dumps(dic,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return response
if __name__=="__main__":
   app.run(port=8080)

