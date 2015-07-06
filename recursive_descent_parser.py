from grammar import Grammar

class RecursiveDescentParser():
	def __init__(self, grammar):
		self._grammar = grammar

		# if not self._grammar.is_ll1:
		# 	raise Exception("Grammar is not LL(1)!")

		self._code = self._parser_code()

	def __repr__(self):
		return self._code

	def _parser_code(self):
		code = "def parser_code(sentence):\n"
		code +="	lexic_analyzer(sentence)\n"
		code +="	" + self._grammar._initial_symbol + "(sentence)\n"
		code +="	if sentence == '$':\n"
		code +="		return True\n"
		code +="	else:\n"
		code +="		raise Exception('Unexpected end of sentence')"

		self._code = code

	def parse(self, sentence):
		exec(self._code,globals())
		return parser_code(sentence)
