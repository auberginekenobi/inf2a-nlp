"""
Test code for all of the functionalities in Inf2a assignment 2
Owen Chapman

"""

import unittest
#from statements import *
#from pos_tagging import *
from agreement import *


global corpus, lx, fb
corpus = Lexicon()
lx = Lexicon()
fb = FactBase()

# Part A Processing statements
class TestA(unittest.TestCase):
    
    def testLexicon1(self):
        corpus.add("duck","P")
        self.assertEquals(corpus.getAll('P'), ['duck'])
        corpus.add("duck","I")
        self.assertEquals(corpus.getAll('I'), ['duck'])
        corpus.add("duck","P")
        self.assertEquals(corpus.getAll('P'), ['duck'])
        corpus.add("goose","P")
        self.assertEquals(corpus.getAll('P'), ['duck','goose'])

    def testLexicon2(self):
        lx = Lexicon()
        lx.add("John","P")
        lx.add("Mary","P")
        lx.add("like","T")
        self.assertEquals(lx.getAll("P"),["John","Mary"])
        
    def testFactBase1(self):
        fb.addUnary("duck","John")
        fb.addBinary("love","John","Mary")
        self.assertTrue(fb.queryUnary("duck","John"))
        self.assertFalse(fb.queryBinary("love","Mary","John"))

    def testVerbStem(self):
        # Examples from handout
        self.assertEquals(verb_stem('has'),'have')
        self.assertEquals(verb_stem('eats'),'eat')
        self.assertEquals(verb_stem('tells'),'tell')
        self.assertEquals(verb_stem('shows'),'show')
        self.assertEquals(verb_stem('pays'),'pay')
        self.assertEquals(verb_stem('buys'),'buy')
        self.assertEquals(verb_stem('flies'),'fly')
        self.assertEquals(verb_stem('tries'),'try')
        self.assertEquals(verb_stem('unifies'),'unify')
        self.assertEquals(verb_stem('dies'),'die')
        self.assertEquals(verb_stem('lies'),'lie')
        self.assertEquals(verb_stem('ties'),'tie')
        self.assertEquals(verb_stem('goes'),'go')
        self.assertEquals(verb_stem('boxes'),'box')
        self.assertEquals(verb_stem('attaches'),'attach')
        self.assertEquals(verb_stem('washes'),'wash')
        self.assertEquals(verb_stem('dresses'),'dress')
        self.assertEquals(verb_stem('fizzes'),'fizz')
        self.assertEquals(verb_stem('loses'),'lose')
        self.assertEquals(verb_stem('dazes'),'daze')
        self.assertEquals(verb_stem('lapses'),'lapse')
        self.assertEquals(verb_stem('analyses'),'analyse')
        self.assertEquals(verb_stem('likes'),'like')
        self.assertEquals(verb_stem('hates'),'hate')
        self.assertEquals(verb_stem('bathes'),'bathe')

        # My own examples
        self.assertEquals(verb_stem('analyzes'),'analyze')
        #self.assertEquals(verb_stem('unties'),'unty')

        # Failures
        self.assertEquals(verb_stem('bob'),'')
        self.assertEquals(verb_stem('cats'),'')
        self.assertEquals(verb_stem('elephants'),'')
        self.assertEquals(verb_stem('its'),'')
        self.assertEquals(verb_stem('this'),'')
        self.assertEquals(verb_stem('Owens'),'')
        self.assertEquals(verb_stem(''),'')

    def testAll(self):
        lx = Lexicon()
        fb = FactBase()
        process_statement(lx,['John','is','a','duck'],fb)
        process_statement(lx,['John','is','blue'],fb)
        process_statement(lx,['John','eats'],fb)
        process_statement(lx,['Mary','loves','John'],fb)
    #truths
        self.assertTrue(fb.queryUnary("N_duck","John"))
        self.assertTrue(fb.queryBinary("T_love","Mary","John"))
        self.assertTrue(fb.queryUnary("I_eat","John"))
        self.assertTrue(fb.queryUnary("A_blue","John"))

    #falses
        self.assertFalse(fb.queryUnary("A_red","John"))
        self.assertFalse(fb.queryUnary("I_drink","John"))
        self.assertFalse(fb.queryUnary("N_goose","John"))
        self.assertFalse(fb.queryBinary("T_love","John","Mary"))

#run tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestA)
unittest.TextTestRunner(verbosity=2).run(suite)


#setup lexicon
lx = Lexicon()
lx.add("John","P")
lx.add("Mary","P")
lx.add("like","T")
lx.add("eat","I")
lx.add("eat","T")
lx.add("blue","A")
lx.add("duck","N")
lx.add("duck","I")
lx.add("sheep","N")
lx.add("woman","N")
lx.add("have","T")
lx.add("die","I")
lx.add("go","I")
lx.add("go","T")
# Testing part B: POS tagging
class TestB(unittest.TestCase):
    
    def testNounStem(self):
        #plurals
        self.assertEquals(noun_stem('series'),'series')
        self.assertEquals(noun_stem('men'),'man')
        self.assertEquals(noun_stem('sheep'),'sheep')
        self.assertEquals(noun_stem('moose'),'moose')
        self.assertEquals(noun_stem('women'),'woman')
        self.assertEquals(noun_stem('basemen'),'baseman')
        self.assertEquals(noun_stem('bobs'),'bob')
        self.assertEquals(noun_stem('cats'),'cat')
        self.assertEquals(noun_stem('elephants'),'elephant')
        self.assertEquals(noun_stem('its'),'it')
        self.assertEquals(noun_stem('this'),'thi')
        self.assertEquals(noun_stem('glass'),'glas')
        self.assertEquals(noun_stem('glasses'),'glasse')
        #Non-plurals
        self.assertEquals(noun_stem('bob'),'')
        self.assertEquals(noun_stem('cat'),'')
        self.assertEquals(noun_stem('Illuminati'),'')
        self.assertEquals(noun_stem('these'),'')
        self.assertEquals(noun_stem(''),'')
        self.assertEquals(noun_stem('nuclei'),'')

    def testTagWord(self):

        print 'John', tag_word(lx,'John')
        print 'likes', tag_word(lx,'likes')
        print 'like', tag_word(lx,'like')
        print 'has', tag_word(lx,'has')
        print 'have', tag_word(lx,'have')
        print 'sheep', tag_word(lx,'sheep')
        print 'women', tag_word(lx,'women')
        print 'duck', tag_word(lx,'duck')
        print 'ducks', tag_word(lx,'ducks')
        
        self.assertEquals(set(tag_word(lx, 'goes')),set(['Ts','Is']))
        self.assertEquals(set(tag_word(lx, 'blue')),set(['A']))
        self.assertEquals(set(tag_word(lx, 'duck')),set(['Ns','Ip']))
        self.assertEquals(set(tag_word(lx, 'ducks')),set(['Np','Is']))

print "Manual check: unchanging plurals list:"
print unchanging_plurals_list
suite = unittest.TestLoader().loadTestsFromTestCase(TestB)
unittest.TextTestRunner(verbosity=2).run(suite)

class TestC(unittest.TestCase):
    def testNPhraseNum(self):
        print all_parses(['John','is','a','duck'],lx)
        print all_valid_parses(lx,['John','is','a','duck'])
        
        
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestC)
unittest.TextTestRunner(verbosity=2).run(suite)        





print fb.items()

