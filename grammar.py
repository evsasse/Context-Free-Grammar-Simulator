class Grammar():
	__possible_nonterminals = set("ABCDEFGHIJKLMNOPQRSTUVXWYZ")

	def __init__(self, terminals = {'a','b','c','d','0','1','2','3','&'}, nonterminals = __possible_nonterminals, initial_symbol = 'S'):
		self._productions = set()
		self._terminals = terminals
		self._nonterminals = nonterminals
		self._initial_symbol = initial_symbol

		if self._initial_symbol not in self._nonterminals:
			raise Exception("Initial symbol not in nonterminals!")


	def __repr__(self):
		st = ''
		for nonterminal in [self._initial_symbol]+list(self._nonterminals-{self._initial_symbol}):
			if nonterminal != self._initial_symbol:
				st += "\n"
			st += "%s -> "%(nonterminal)
			rights = [production.right for production in self._productions if production.left == nonterminal]
			for right in rights[:-1]:
				st += "%s | "%(right)
			st += "%s"%(rights[-1])

		return st

	def _first(self, symbols):
		# CAN EASILY CAUSE STACK OVERFLOW WHEN THERE IS LEFT RECURSION OR IS NOT LEFT FACTORED
		# Not a problem if called just on _have_first_follow_conflict
		# because it's called just after a check for left recursion and left factoring

		# Expecting a list of symbols. Otherwise, if it's a string, split on spaces
		if not isinstance(symbols,list):
			symbols = symbols.split(' ')

		try:
			if symbols[0] == '&' and len(symbols) > 1:
				return self._first(symbols[1:])
			if symbols[0] in self._terminals:
				return {symbols[0]}
			if symbols[0] in self._nonterminals:
				# union of all first sets of productions related to symbol[0]
				firsts = set.union(*[self._first(production.right) for production in self._productions if production.left == symbols[0]])
				if '&' in firsts and len(symbols) > 1:
					firsts -= {'&'}
					firsts |= self._first(symbols[1:])
				return firsts
		except RuntimeError:
			raise Exception("Should check for Left Factoring and against Left Recursion before calling _first")

	def _follow(self, symbol):
		pass

	def is_ll1(self):
		return self._have_left_recursion() and self._is_left_factored() and self._have_first_follow_conflict()

	def _have_left_recursion(self):
		pass

	def _is_left_factored(self):
		pass

	def _have_first_follow_conflict(self):
		pass

	@staticmethod
	def text_to_grammar(text):
		# TAKE ACCOUNT OF 2nd OBSERVATION

		terminals = set()
		nonterminals = set()
		initial_symbol = None
		productions = set()

		for line in text.split('\n'):
			line = line.replace(' ','')
			(left, rights) = line.split('->')

			nonterminals |= {left}

			if initial_symbol == None:
				initial_symbol = left

		for line in text.split('\n'):
			(left, rights) = line.split('->')
			left = left.replace(' ','')

			for right in rights.split('|'):
				right = right.strip()
				terminals |= {symbol for symbol in right.split(' ') if symbol not in nonterminals}
				productions |= {Production(left,right.split(' '))}

		# if terminals & Grammar.__possible_nonterminals != set():
		# 	raise Exception("Possible non-terminal used without productions related to it!")

		grammar = Grammar(terminals, nonterminals, initial_symbol)
		grammar._productions = productions

		return grammar

class ProductionRightList(list):
	def __repr__(self):
		st = ''
		for each in self[:-1]:
			st += "%s "%(each)
		st += "%s"%(self[-1])
		return st

class Production():
	def __init__(self, left, right):
		self.left = left

		if isinstance(right, list):
			self.right = ProductionRightList(right)
		else:
			self.right = ProductionRightList(right.split(' '))

	def __repr__(self):
		return "%s -> %s"%(self.left, self.right)

	def __hash__(self):
		return hash(self.__repr__())

	def __eq__(self, other):
		return self.left == other.left and self.right == other.right
