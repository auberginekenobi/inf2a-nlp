# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here
    def __init__(self):
        self.lexicon = {"P":[], "N":[], "A":[], "I":[], "T":[]}

    def add(self, stem, cat):
        if stem not in self.lexicon[cat]:
            self.lexicon[cat].append(stem)

    def getAll(self, cat):
        return self.lexicon[cat]
    

class FactBase:
    """stores a database of facts"""
    # add code here
    def __init__(self):
        self.db = []
    def addUnary(self,pred,e1):
        if (pred, e1) not in self.db:
            self.db.append((pred, e1))
    def queryUnary(self,pred,e1):
        return (pred, e1) in self.db
    def addBinary(self,pred,e1,e2):
        if (pred, e1, e2) not in self.db:
            self.db.append((pred,e1,e2))
    def queryBinary(self,pred,e1,e2):
        return (pred, e1, e2) in self.db

    def items(self):
        return self.db
    

import re
from nltk.corpus import brown
re1 = re.compile('[A-z]*[^sxyzaeiou]s$|[A-z]*[^sc]hs$')
re2 = re.compile('[A-z]*[aeiou]ys$')
re3 = re.compile('[A-z][A-z]+ies$')
re4 = re.compile(r'\A[A-z]ies$')
re5 = re.compile('[A-z]*([ox]es|[cs]hes|sses|zzes)$')
re6 = re.compile('[A-z]*([^s]ses|[^z]zes)$')
re7 = re.compile(r'\Ahas$')
re8 = re.compile('[A-z]*([^iosxz]es|[^cs]hes)$')

# making a dictionary for faster search
posdict = {}
brownwords = set(brown.tagged_words())
for (word, pos) in brownwords:
    if word in posdict:
        posdict[word].append(pos)
        posdict[word] = list(set(posdict[word]))
    else:
        posdict[word] = [pos]
        
# for testing purposes. 'ducks' is a very important verb in my test cases.
##posdict['analyses']='VBZ'
##posdict['fizzes'] = 'VBZ'
##posdict['boxes'] = 'VBZ'
##posdict['washes'] = 'VBZ'
##posdict['dresses'] = 'VBZ'
##posdict['dazes'] = 'VBZ'
##posdict['bathes'] = 'VBZ'
##posdict['ducks'] = 'VBZ'
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # add code here
    # case 7 - has --> have
    if re.match(re7,s):
        return 'have'
    if (s in posdict and ('VBZ' in posdict[s])) or s=='does':
        # case 3 - flies --> fly
        if re.match(re3,s):
            return s[:-3]+'y'
        # case 5 - goes --> go
        if re.match(re5,s):
            return s[:-2]
        # case 1 - eats --> eat
        if re.match(re1,s):
            return s[:-1]
        # case 2 - pays --> pay
        if re.match(re2,s):
            return s[:-1]
        # case 4 - dies --> die
        if re.match(re4,s):
            return s[:-1]
        # case 6 - analyzes --> analyze
        if re.match(re6,s):
            return s[:-1]
        # case 8 - likes --> like
        if re.match(re8,s):
            return s[:-1]
    return ""
    

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

