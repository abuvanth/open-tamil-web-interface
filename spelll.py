from opentamiltests import *
from spell import Speller, LoadDictionary
from tamil import utf8
import os
from flask import Flask,request,json,Response
app=Flask(__name__)
@app.route("/")
def index():
     return "get request"
@app.route("/<k1>")
def spell_check(k1):
    speller =  Speller(lang=u"TA",mode="web")
    notok,suggs = speller.check_word_and_suggest( k1 )
    json_string = json.dumps(suggs,ensure_ascii = False)
    #creating a Response object to set the content type and the encoding
    response = Response(json_string,content_type="application/json; charset=utf-8" )
    return responseபுகழ்
if __name__=="__main__":
   app.run(port=8080)

