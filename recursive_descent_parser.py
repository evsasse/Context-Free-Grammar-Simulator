from grammar import Grammar

class RecursiveDescentParser():
	def __init__(self, grammar):
		self._grammar = grammar

		if not self._grammar.is_ll1:
			raise Exception("Grammar is not LL(1)!")


	def __repr__(self):
		return self.parse_code()


	def parse(self, sentence):
		# will maintain all the functions generated in this dict scope
		parser_wrapper = {}
		exec(self.parser_code(), parser_wrapper)
		return parser_wrapper['main'](sentence)


	def parser_code(self):
		code = ''
		code = self._parser_code_main()
		code += self._parser_code_next_lexic_symbol()
		for nonterminal in sorted(self._grammar._nonterminals):
			code += self._parser_code_nonterminal(nonterminal).strip()+'\n\n'
		return code


	def _parser_code_main(self):
		code = '''\
def main(sentence):
	global _sentence
	global _current_symbol_position
	_sentence = (sentence.strip() + ' $').split(' ')
	_current_symbol_position = -1
	global current_symbol

	next_lexic_symbol()

	%s()

	if current_symbol == '$':
		return True
	raise Exception('PARSING','$',current_symbol)'''
		code = code%(self._grammar._initial_symbol)+"\n\n"
		return code

	def _parser_code_next_lexic_symbol(self):
		code = '''\
def next_lexic_symbol():
	global _sentence
	global _current_symbol_position
	global current_symbol

	_current_symbol_position += 1
	current_symbol = _sentence[_current_symbol_position]'''
		return code+'\n\n'


	def _parser_code_nonterminal(self,nonterminal):
		code = '''def %s():\n'''%(nonterminal)
		code += '''\tglobal current_symbol\n'''
		#code += '''\tglobal _sentence\n'''
		#code += '''\tglobal _current_symbol_position\n'''
		#code += '''\tprint('%s',_sentence,_current_symbol_position,current_symbol)\n'''%(nonterminal)

		productions_of_nonterminal = sorted([p for p in self._grammar._productions if p.left == nonterminal])
		should_do_else = '&' not in self._grammar._first(nonterminal)

		# in the special case of having just one production and it is to &, return "pass"
		if len(productions_of_nonterminal) == 1 and productions_of_nonterminal[0].right == ['&']:
			code += "\tpass\n\n"
			return code

		if_or_elif = "if"
		# do the productions that arent &
		for production in productions_of_nonterminal:
			if production.right != ['&']:
				code += '''\t%s current_symbol in %s:\n'''%(if_or_elif,sorted(self._grammar._first(production.right)))
				if_or_elif = "elif"
				for line in self._parser_code_production(production,nonterminal).split('\n'):
					code += '''\t%s\n'''%(line)
		if should_do_else:
			code += '''\telse:\n\t\traise Exception('PARSING','%s',%s,current_symbol)\n\n'''%(nonterminal,sorted(self._grammar._first(nonterminal)))
		return code


	def _parser_code_production(self,production,nonterminal):
		code = ''''''
		for symbol in production.right:
			if symbol != '&':
				for line in self._parser_code_symbol(symbol,production,nonterminal).split('\n'):
					code += '''\t%s\n'''%(line)
		return code


	def _parser_code_symbol(self,symbol,production,nonterminal):
		if symbol in self._grammar._terminals:
			code = '''\
if current_symbol == '%s':
	next_lexic_symbol()
else:
	raise Exception('PARSING','%s','%s',current_symbol)'''
			code = code%(symbol, nonterminal, symbol)
		elif symbol in self._grammar._nonterminals:
			code =	'''%s()'''
			code = code%(symbol)
		return code
