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

	def _first(self, symbols, log = None):
		# CAN EASILY CAUSE STACK OVERFLOW WHEN THERE IS LEFT RECURSION
		# Not a problem if called just on _have_first_follow_conflict
		# because it's called just after a check for left recursion

		# Expecting a list of symbols. Otherwise, if it's a string, split on spaces
		if not isinstance(symbols,list):
			symbols = symbols.strip()
			symbols = symbols.split(' ')

		if log != None:
			log('Fazendo first de "%s"'%(' '.join(symbols)))

		try:
			if symbols == []:
				if log != None:
					log('= %s'%({'&'}))
				return {'&'}
			if symbols[0] == '&' and len(symbols) > 1:
				firsts = self._first(symbols[1:])
				if log != None:
					log('= %s'%(firsts))
				return firsts
			if symbols[0] in self._terminals:
				if log != None:
					log('= %s'%({symbols[0]}))
				return {symbols[0]}
			if symbols[0] in self._nonterminals:
				# union of all first sets of productions related to symbol[0]
				firsts = set.union(*[self._first(production.right) for production in self._productions if production.left == symbols[0]])
				if '&' in firsts and len(symbols) > 1:
					firsts -= {'&'}
					firsts |= self._first(symbols[1:])
				if log != None:
					log('= %s'%(firsts))
				return firsts
		except RuntimeError:
			raise Exception("Should check against Left Recursion before calling _first")

	def _follow(self, symbol, log = None):
		if symbol not in self._nonterminals:
			raise Exception("Symbol should be on the nonterminals")

		if log != None:
			log('Fazendo follow de "%s"'%(symbol))

		follow = {}
		_follow = {}
		for nonterminal in self._nonterminals:
			follow[nonterminal] = set()
		follow[self._initial_symbol] = {'$'}

		for production in self._productions:
			# for each nonterminal on the production-right
			for (position, nonterminal) in [(p,s) for (p,s) in enumerate(production.right) if s in self._nonterminals]:
				# add the first of the remainder right side after it to its follow
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

	def is_ll1(self, log = None):
		return not self._have_left_recursion(log) and self._is_left_factored(log) and not self._have_first_follow_conflict(log)

	def _have_left_recursion(self, log = None):
		if log != None:
			log('Verificando recursão à esquerda')
		# unfortunately the only way I've found to make ir work :/

		nts_leads_to_lr = set()

		for nt in self._nonterminals:
			try:
				self._first([nt],log)
			except Exception:
				#print(nt)
				nts_leads_to_lr |= {nt}

		if nts_leads_to_lr == set():
			return False

		raise Exception('LEFT_RECURSION',nts_leads_to_lr)

	def _is_left_factored(self, log = None):
		if log != None:
			log('Verificando fatoração')

		firsts = {}

		nts_non_left_factored = set()

		# for each production
		for production in self._productions:
			if production.left in nts_non_left_factored:
				continue
			# adds its _first in a set related to the production-left
			if production.left not in firsts:
				firsts[production.left] = self._first(production.right,log)
			else:
				_first = self._first(production.right,log)
				# if there is any intersection between firsts of a same nonterminal
				if _first & firsts[production.left]:
					# then it's not left factored
					#return False
					nts_non_left_factored |= {production.left}
					continue
				firsts[production.left] |= _first

		if nts_non_left_factored != set():
			raise Exception('LEFT_FACTORING',nts_non_left_factored)

		# if it ends the loop and none intersection was found
		# then is left factored
		return True

	def _have_first_follow_conflict(self, log = None):
		if log != None:
			log('Verificando conflito first/follow')

		nts_with_conflict = set()

		# for each nonterminal that can reach &
		for nonterminal in [nt for nt in self._nonterminals if '&' in self._first(nt,log)]:
			# if there is an intersection between its first and follow
			if self._first(nonterminal,log) & self._follow(nonterminal):
				#return True
				nts_with_conflict |= {nonterminal}

		if nts_with_conflict != set():
			raise Exception('FIRST_FOLLOW_CONFLICT',nts_with_conflict)

		# if there isnt any intersection between the first and follow of
		# nonterminals that can reach &, then there is no conflict
		return False

	@staticmethod
	def text_to_grammar(text):

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
				# any symbol that isnt on production-left of any line is considered terminal
				terminals |= {symbol for symbol in right.split(' ') if symbol not in nonterminals}
				productions |= {Production(left,right.split(' '))}

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

	def __lt__(self, other):
		if self.left != other.left:
			return False
		self.right < other.right
