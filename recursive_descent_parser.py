from grammar import Grammar

class RecursiveDescentParser():
	def __init__(self, grammar):
		self._grammar = grammar

		if not self._grammar.is_ll1:
			raise Exception("Grammar is not LL(1)!")

	def __repr__(self):
		return self.parse_code()

	def parser_code(self):
		return _parser_code_non_terminal(self._grammar._initial_symbol)
		# code = "def parser_code(sentence):\n"
		# code +="	lexic_analyzer(sentence)\n"
		# code +="	" + self._grammar._initial_symbol + "(sentence)\n"
		# code +="	if sentence == '$':\n"
		# code +="		return True\n"
		# code +="	else:\n"
		# code +="		raise Exception('Unexpected end of sentence')"
		#
		# self._code = code

	def _parser_code_non_terminal(self,nonterminal):
		code = '''def %s(current_symbol):'''%(nonterminal)

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
	current_symbol = next_lexic_symbol()
else:
	raise Exception('%s','%s',current_symbol)'''
			code = code%(symbol, nonterminal, symbol)
		elif symbol in self._grammar._nonterminals:
			code =	'''%s(current_symbol)'''
			code = code%(symbol)
		return code

	def parse(self, sentence):
		parser_wrapper = {}

		exec(self._code, parser_wrapper)

		return parser_wrapper.main(sentence)
