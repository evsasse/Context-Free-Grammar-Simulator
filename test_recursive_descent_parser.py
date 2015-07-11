import unittest
from recursive_descent_parser import RecursiveDescentParser
from grammar import Grammar
from grammar import Production

class TestRecursiveDescentParser(unittest.TestCase):

	def test_parser_code_production(self):
		s = "S -> A B C\n"
		s +="A -> a A | &\n"
		s +="B -> b B | A C d\n"
		s +="C -> c C | &"
		g = Grammar.text_to_grammar(s)
		r = RecursiveDescentParser(g)

		c = '''\
	A(current_symbol)
	B(current_symbol)
	C(current_symbol)
'''
		self.assertEqual(c,r._parser_code_production(Production('S','A B C'),'S'))

		c = '''\
	if current_symbol == 'a':
		current_symbol = next_lexic_symbol()
	else:
		raise Exception('A','a',current_symbol)
	A(current_symbol)
'''
		self.assertEqual(c,r._parser_code_production(Production('A','a A'),'A'))

		c = '''\
	A(current_symbol)
	C(current_symbol)
	if current_symbol == 'd':
		current_symbol = next_lexic_symbol()
	else:
		raise Exception('B','d',current_symbol)
'''
		self.assertEqual(c,r._parser_code_production(Production('B','A C d'),'B'))
