import unittest
from grammar import Grammar
from grammar import Production

class TestGrammar(unittest.TestCase):

	def test_text_to_grammar(self):
		s = "S -> a"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._productions, {Production('S','a')})

		s = "S -> b S | a"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._productions, {Production('S','a'), Production('S',['b','S'])})

		s = "S1 -> b S1 a | a"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._productions, {Production('S1','a'), Production('S1',['b','S1','a'])})

		s = "C -> if E then C C' | comando\nC' -> else C | &\nE -> exp"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._productions, {Production("C","if E then C C'"), Production("C","comando"), Production("C'","else C"), Production("C'","&"), Production("E","exp")})

	def test_first(self):
		s = "S -> a"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._first('S'),{'a'})
		self.assertEqual(g._first('a'),{'a'})
		self.assertEqual(g._first('a b S c S t e'),{'a'})

		s = "S -> b S | a"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._first('S'),{'a','b'})

		s = "S1 -> b S1 a | a"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._first("S1"),{'a','b'})

		s = "C -> if E then C C' | comando\nC' -> else C | &\nE -> exp"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._first("C"),{'if','comando'})
		self.assertEqual(g._first("C'"),{'else','&'})
		self.assertEqual(g._first("E"),{'exp'})
		self.assertEqual(g._first("E C"),{'exp'})
		self.assertEqual(g._first("C' E"),{'else','exp'})
