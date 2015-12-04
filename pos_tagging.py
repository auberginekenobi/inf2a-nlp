# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    uplist = []
    ndict = {}
    with open("sentences.txt", "r") as f:
        for line in f:
            # add code here
            line = line.split()
            for pair in line:
                wordpos = pair.split('|') # [word, pos]
                word = wordpos[0]
                pos = wordpos[1]
                if pos == 'NN':
                    if word in ndict and ndict[word]=='NNS':
                        uplist.append(word)
                elif pos == 'NNS':
                    if word in ndict and ndict[word]=='NN':
                        uplist.append(word)
                ndict[word] = pos
    return list(set(uplist))
                    
            
            

unchanging_plurals_list = unchanging_plurals()
ren = re.compile('\A[A-z]*men$') 
def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    # add code here
    # NB this will recognize verbs such as 'bathes' and turn them into 'bathe'
    # NB this will also fail for plural nouns like 'glasses' --> 'glasse'
    if s in unchanging_plurals_list:
        return s
    if re.match(ren, s):
        return s[:-2]+'an'
    if s!='' and s[-1]=='s':
        return s[:-1]
    return ''
    

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here
    posspos = [] # possible parts of speech
    # check special words
    for pair in function_words_tags:
        if wd == pair[0]:
            posspos.append(pair[1])
    # check lexicon
    nwd = noun_stem(wd)
    vwd = verb_stem(wd)
    for char in 'PNAIT':
        if wd in lx.getAll(char) or nwd in lx.getAll(char) or vwd in lx.getAll(char):
            if char == 'P' or char == 'A':
                posspos.append(char)
            elif char == 'N':
                if nwd!='':
                    #plural
                    posspos.append('Np')
                else:
                    #singular
                    posspos.append('Ns')
                if wd in unchanging_plurals_list:
                    #singular and plural, but only need to add singular
                    posspos.append('Ns')
            elif char == 'I' or char == 'T':
                if vwd!='':
                    posspos.append(char+'s')
                else:
                    posspos.append(char+'p')
    return list(set(posspos))
                

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
