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

		s = "C -> if E then C C' | comando\n"
		s +="C' -> else C | &\n"
		s +="E -> exp"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._productions, {Production("C","if E then C C'"), Production("C","comando"),\
		 Production("C'","else C"), Production("C'","&"), Production("E","exp")})

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

		s = "C -> if E then C C' | comando\n"
		s +="C' -> else C | &\n"
		s +="E -> exp"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._first("C"),{'if','comando'})
		self.assertEqual(g._first("C'"),{'else','&'})
		self.assertEqual(g._first("E"),{'exp'})
		self.assertEqual(g._first("E C"),{'exp'})
		self.assertEqual(g._first("C' E"),{'else','exp'})

		s = "S -> A b | A B c\n"
		s +="B -> b B | A d | &\n"
		s +="A -> a A | &"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._first("S"),{'a','b','c','d'})
		self.assertEqual(g._first("B"),{'a','b','d','&'})
		self.assertEqual(g._first("A"),{'a','&'})

		s = "S -> A B C\n"
		s +="A -> a A | &\n"
		s +="B -> b B | A C d\n"
		s +="C -> c C | &"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._first("S"),{'a','b','c','d'})
		self.assertEqual(g._first("B"),{'b','a','c','d'})
		self.assertEqual(g._first("A"),{'a','&'})
		self.assertEqual(g._first("C"),{'c','&'})


	def test_follow(self):
		s = "S -> a"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._follow('S'),{'$'})

		s = "S -> b S | a"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._follow('S'),{'$'})

		s = "S1 -> b S1 a | a"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._follow("S1"),{'$','a'})

		s = "C -> if E then C C' | comando\n"
		s +="C' -> else C | &\n"
		s +="E -> exp"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._follow("C"),{'$','else'})
		self.assertEqual(g._follow("C'"),{'$','else'})
		self.assertEqual(g._follow("E"),{'then'})

		s = "S -> A b | A B c\n"
		s +="B -> b B | A d | &\n"
		s +="A -> a A | &"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._follow("S"),{'$'})
		self.assertEqual(g._follow("B"),{'c'})
		self.assertEqual(g._follow("A"),{'a','b','c','d'})

		s = "S -> A B C\n"
		s +="A -> a A | &\n"
		s +="B -> b B | A C d\n"
		s +="C -> c C | &"
		g = Grammar.text_to_grammar(s)
		self.assertEqual(g._follow("S"),{'$'})
		self.assertEqual(g._follow("B"),{'c','$'})
		self.assertEqual(g._follow("A"),{'a','b','c','d'})
		self.assertEqual(g._follow("C"),{'d','$'})

	def test_have_left_recursion(self):
		s = "A -> F C a | E A\nB -> C G h\nC -> D B a | b h | c | epsilon\nD -> F e | epsilon\nE -> G h | D f\nF -> E A | d F | epsilon\nG -> g"
		g = Grammar.text_to_grammar(s)
		pass

	def test_is_left_factored(self):
		pass

	def test_have_first_follow_conflict(self):
		pass
