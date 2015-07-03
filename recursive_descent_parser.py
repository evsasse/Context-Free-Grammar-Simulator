class RecursiveDescentParser():
	def __init__(self, grammar):
		self._grammar = grammar

		if not self._grammar.is_ll1:
			raise Exception("Grammar is not LL(1)!")

		self._code = _parser_code()

	def __repr__(self):
		return self._code

	def _parser_code(self):
		pass

	def parse(self, sentence):
		exec(self._code)
		return parser_code(sentence)
