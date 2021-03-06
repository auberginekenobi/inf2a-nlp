"""
Test code for all of the functionalities in Inf2a assignment 2
Owen Chapman

"""

import unittest
#from statements import *
#from pos_tagging import *
from semantics import *


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
lx.add('purple','A')
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
        #NP agreement, AN agreement
        a = all_parses(['who','is','a','purple','duck','?'],lx)
        b = all_valid_parses(lx,['who','is','a','purple','duck','?'])
        self.assertEquals(a,b)
        #print tag_words(lx,['who','is','a','purple','duck','?'])
        self.assertNotEqual(a,[])
        a = all_parses(['who','are','purple','ducks','?'],lx)
        b = all_valid_parses(lx,['who','are','purple','ducks','?'])
        self.assertEquals(a,b)
        self.assertNotEqual(a,[])
        b = all_valid_parses(lx,['who','is','a','purple','ducks','?'])
        self.assertEquals(b,[])
        b = all_valid_parses(lx,['who','are','purple','duck','?'])
        self.assertEquals(b,[])

    def testVPhraseNum(self):
        #Rel agreement, rel structure
        a = all_parses(['who','is','a','duck','John','eats','?'],lx)
        b = all_valid_parses(lx,['who','is','a','duck','John','eats','?'])
        self.assertEquals(a,b)
        self.assertNotEqual(a,[])
        b = all_valid_parses(lx,['who','is','a','duck','John','ducks','?'])
        self.assertEquals(b,[])
        b = all_valid_parses(lx,['who','is','a','duck','John','eat','?'])
        # but maybe this should pass...
        self.assertEquals(b,[])
        a = all_parses(['who','is','a','duck','who','ducks','?'],lx)
        b = all_valid_parses(lx,['who','is','a','duck','who','ducks','?'])
        self.assertEquals(a,b)
        self.assertNotEqual(a,[])
        b = all_valid_parses(lx,['who','is','a','duck','who','duck','?'])
        self.assertEquals(b,[])
        b = all_valid_parses(lx,['who','is','a','duck','who','has','?'])
        self.assertEquals(b,[])

        #VP, BE
        a = all_parses(['which','duck','ducks','and','dies','?'],lx)
        b = all_valid_parses(lx,['which','duck','ducks','and','dies','?'])
        self.assertEquals(b,a)
        self.assertNotEqual(a,[])
        a = all_parses(['which','ducks','duck','and','die','?'],lx)
        b = all_valid_parses(lx,['which','ducks','duck','and','die','?'])
        self.assertEquals(b,a)
        self.assertNotEqual(a,[])
        b = all_valid_parses(lx,['which','sheep','ducks','and','die','?'])
        self.assertEquals(b,[])
        b = all_valid_parses(lx,['which','sheep','ducks','and','die','?'])
        self.assertEquals(b,[])

        a = all_parses(['who','are','ducks','?'],lx)
        b = all_valid_parses(lx,['who','are','ducks','?'])
        self.assertEquals(a,b)
        self.assertNotEqual(a,[])
        b = all_valid_parses(lx,['who','are','duck''?'])
        self.assertEquals(b,[])
        b = all_valid_parses(lx,['who','is','ducks''?'])
        self.assertEquals(b,[])

'''        print tag_words(lx,['who','does','John','like','?'])
        print all_parses(['who','does','John','like','?'],lx)
        print all_valid_parses(lx,['who','does','John','like','?'])
        print all_parses(['who','does','John','likes','?'],lx)
        print all_valid_parses(lx,['who','does','John','likes','?'])
        print all_parses(['Does','John','like','ducks'],lx)
        print all_parses(['Does','John','like','ducks','?'],lx)
        print all_valid_parses(lx,['is','John','a','duck','?'])
        '''
        
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestC)
unittest.TextTestRunner(verbosity=2).run(suite)


def runAll(wdlst):
    tr0 = all_valid_parses(lx,wdlst)[0]
    tr = restore_words(tr0,wdlst)
    A = lp.parse(sem(tr))
    print A.simplify()
    
tr0 = all_valid_parses(lx, ['Who','is','a','purple','duck','?'])[0]
#tr0.draw()
tr = restore_words(tr0,['Who','is','a','purple','duck','?'])

#A = lp.parse(sem(tr0))
B = lp.parse(sem(tr))  # for some tree tr
#print A.simplify()
print B.simplify()
tr0 = all_valid_parses(lx, ['Who','is','John','?'])[0]
tr = restore_words(tr0,['Who','is','John','?'])
A = lp.parse(sem(tr))
print A.simplify()

runAll('Who is blue ?'.split())
runAll('Who ducks and dies ?'.split())
runAll('Who does John like ?'.split())
runAll('Which purple duck likes a woman ?'.split())
runAll('Which purple duck likes John ?'.split())
runAll('Who is a woman who ducks ?'.split())
runAll('Who is a woman John eats ?'.split())
runAll('Who is a woman ducks eat ?'.split())
runAll('Who is a woman who eats ducks ?'.split())

