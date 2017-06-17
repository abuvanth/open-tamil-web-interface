# -*- coding: utf-8 -*-
# (C) 2016 Muthiah Annamalai

from opentamiltests import *
from spell import Speller, LoadDictionary
from pprint import pprint
import os
from tamil import utf8
def test_words_in_error():
        # test if the words in error are flagged
        # further test if suggestion contains the right word
    speller =  Speller(lang=u"TA",mode="web")
    words_and_fixes = { u"எந்திர" : u"எந்திரம்",
                            u"செயல்பட":u"செயல்"}
    for w,right_word in words_and_fixes.items():
        notok,suggs = speller.check_word_and_suggest( w )
    print suggs[2]
