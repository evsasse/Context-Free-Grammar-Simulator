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
	A()
	B()
	C()'''
		self.assertEqual(c.strip(),r._parser_code_production(Production('S','A B C'),'S').strip())

		c = '''\
	if current_symbol == 'a':
		next_lexic_symbol()
	else:
		raise Exception('A','a',current_symbol)
	A()'''
		self.assertEqual(c.strip(),r._parser_code_production(Production('A','a A'),'A').strip())

		c = '''\
	A()
	C()
	if current_symbol == 'd':
		next_lexic_symbol()
	else:
		raise Exception('B','d',current_symbol)'''
		self.assertEqual(c.strip(),r._parser_code_production(Production('B','A C d'),'B').strip())

	def test_parser_code_nonterminal(self):
		s = "S -> A B C\n"
		s +="A -> a A | &\n"
		s +="B -> b B | A C d\n"
		s +="C -> c C | D\n"
		s +="D -> &"
		g = Grammar.text_to_grammar(s)
		r = RecursiveDescentParser(g)

		c = '''\
def S():
	global current_symbol
	if current_symbol in ['a', 'b', 'c', 'd']:
		A()
		B()
		C()
\t
	else:
		raise Exception('S',['a', 'b', 'c', 'd'],current_symbol)'''
		self.assertEqual(c.strip(),r._parser_code_nonterminal('S').strip())

		c = '''\
def A():
	global current_symbol
	if current_symbol in ['a']:
		if current_symbol == 'a':
			next_lexic_symbol()
		else:
			raise Exception('A','a',current_symbol)
		A()'''
		self.assertEqual(c.strip(),r._parser_code_nonterminal('A').strip())

# def main(sentence):
#         global _sentence
#         global _current_symbol_position
#         _sentence = (sentence + ' $').strip().split(' ')
#         _current_symbol_position = -1
#         global current_symbol
#
#         next_lexic_symbol()
#
#         S()
#
#         if current_symbol == '$':
#                 return True
#         raise Exception('Unexpected end','$',current_symbol)
#
# def next_lexic_symbol():
#         global _sentence
#         global _current_symbol_position
#         global current_symbol
#
#         _current_symbol_position += 1
#         current_symbol = _sentence[_current_symbol_position]
#
# def A():
#         global current_symbol
#         if current_symbol in ['a']:
#                 if current_symbol == 'a':
#                         next_lexic_symbol()
#                 else:
#                         raise Exception('A','a',current_symbol)
#                 A()
#
# def B():
#         global current_symbol
#         if current_symbol in ['a', 'c', 'd']:
#                 A()
#                 C()
#                 if current_symbol == 'd':
#                         next_lexic_symbol()
#                 else:
#                         raise Exception('B','d',current_symbol)
#
#         elif current_symbol in ['b']:
#                 if current_symbol == 'b':
#                         next_lexic_symbol()
#                 else:
#                         raise Exception('B','b',current_symbol)
#                 B()
#
#         else:
#                 raise Exception('B',['a', 'b', 'c', 'd'],current_symbol)
#
# def C():
#         global current_symbol
#         if current_symbol in ['c']:
#                 if current_symbol == 'c':
#                         next_lexic_symbol()
#                 else:
#                         raise Exception('C','c',current_symbol)
#                 C()
#
#         elif current_symbol in ['&']:
#                 D()
#
# def D():
#         global current_symbol
#         pass
#
# def S():
#         global current_symbol
#         if current_symbol in ['a', 'b', 'c', 'd']:
#                 A()
#                 B()
#                 C()
#
#         else:
#                 raise Exception('S',['a', 'b', 'c', 'd'],current_symbol)
