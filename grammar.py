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
		# CAN EASILY CAUSE STACK OVERFLOW WHEN THERE IS LEFT RECURSION
		# Not a problem if called just on _have_first_follow_conflict
		# because it's called just after a check for left recursion

		# Expecting a list of symbols. Otherwise, if it's a string, split on spaces
		if not isinstance(symbols,list):
			symbols = symbols.strip()
			symbols = symbols.split(' ')

		# print("First de", symbols)

		try:
			if symbols == []:
				return {'&'}
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
			raise Exception("Should check against Left Recursion before calling _first")

	def _follow(self, symbol):
		if symbol not in self._nonterminals:
			raise Exception("Symbol should be on the nonterminals")

		follow = {}
		_follow = {}
		for nonterminal in self._nonterminals:
			follow[nonterminal] = set()
		follow[self._initial_symbol] = {'$'}

		for production in self._productions:
			# for each nonterminal on the production-right
			for (position, nonterminal) in [(p,s) for (p,s) in enumerate(production.right) if s in self._nonterminals]:
				# add the first of the remainder right side after it to its follow
				# print("follow de",nonterminal)
				follow[nonterminal] |= self._first(production.right[position+1:])
			# for each nonterminal that has & on its follow
			for nonterminal in [nt for nt in follow if '&' in follow[nt]]:
				# remove & from the follow, and add the production-left nonterminal to its follow
				# this nonterminal will be swapped later
				# also remove the own nonterminal from its follow
				follow[nonterminal] -= {'&'}
				follow[nonterminal] |= {production.left}
				follow[nonterminal] -= {nonterminal}

		while follow != _follow:
			_follow = follow.copy()
			for nonterminal in self._nonterminals:
				# for each nonterminal _nonterminal in the follow of other nonterminal
				for _nonterminal in [nt for nt in follow[nonterminal] if nt in self._nonterminals]:
					# swap _nonterminal for its follow and remove _nonterminal from the follow
					# also remove the own nonterminal from its follow
					follow[nonterminal] -= {_nonterminal}
					follow[nonterminal] |= follow[_nonterminal]
					follow[nonterminal] -= {nonterminal}

		return follow[symbol]

	def is_ll1(self):
		return not self._have_left_recursion() and self._is_left_factored() and not self._have_first_follow_conflict()

	def _have_left_recursion(self):
		pass

	def _is_left_factored(self):
		firsts = {}

		# for each production
		for production in self._productions:
			# adds its _first in a set related to the production-left
			if production.left not in firsts:
				firsts[production.left] = self._first(production.right)
			else:
				_first = self._first(production.right)
				# if there is any intersection between firsts of a same nonterminal
				if _first & firsts[production.left]:
					# then it's not left factored
					return False
				firsts[production.left] |= _first

		# if it ends the loop and none intersection was found
		# then is left factored
		return True

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
