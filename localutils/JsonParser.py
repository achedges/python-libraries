class JsonParser:
	def __init__(self, jsonstring):
		self.i = 0
		self.n = len(jsonstring)
		self.input = jsonstring
		self.result = dict()

		self.OPENOBJECT = '{'
		self.CLOSEOBJECT = '}'
		self.OPENLIST = '['
		self.CLOSELIST = ']'
		self.COLON = ':'
		self.COMMA = ','
		self.DOUBLEQUOTE = '"'
		self.WHITESPACE = [' ', '\t', '\n', '\r']

	def parse(self):
		self.result = self.parseObject()
		return

	def parseObject(self):
		# an 'object' is some number of key/value pairs, separated by a comma
		obj = dict()

		while self.i < self.n:
			if self.input[self.i] in [self.OPENOBJECT, self.COMMA]:
				# find a key/value pair
				k = self.parseKey()
				v = self.parseValue()

				obj[k] = v

			elif self.input[self.i] == self.CLOSEOBJECT:
				break

			self.i += 1

		return obj

	def parseKey(self):
		# a 'key' is some text identifier enclosed with double quotes
		while self.input[self.i] != self.DOUBLEQUOTE:
			self.i += 1

		self.i += 1
		key = ''

		while self.input[self.i] != self.COLON:
			if self.input[self.i] != self.DOUBLEQUOTE:
				key += self.input[self.i]
			self.i += 1

		self.i += 1
		return key

	def parseValue(self):
		# a 'value' is:
		#	a sub-object ('{...}')
		# 	a list ('[...]')
		#	a quoted identifier
		#	a literal value (1, 12.36, true, ...)
		while self.input[self.i] in self.WHITESPACE:
			self.i += 1  # advance through whitespace

		if self.input[self.i] == self.OPENOBJECT:
			return self.parseObject()

		elif self.input[self.i] == self.OPENLIST:
			return self.parseList()

		elif self.input[self.i] == self.DOUBLEQUOTE:
			return self.parseIdentifier()

		else:
			return self.parseLiteral()

	def parseList(self):
		while self.input[self.i] in (self.WHITESPACE + [self.OPENLIST]): self.i += 1  # advance through whitespace and '['

		lst = list()

		while self.input[self.i] != self.CLOSELIST:
			# is it a new object?
			if self.input[self.i] == self.OPENOBJECT:
				lst.append(self.parseObject())

			# is it a quoted identifier?
			elif self.input[self.i] == self.DOUBLEQUOTE:
				lst.append(self.parseIdentifier())

			self.i += 1

		return lst

	def parseIdentifier(self):
		self.i += 1

		identifier = ''

		while self.input[self.i] != self.DOUBLEQUOTE:
			identifier += self.input[self.i]
			self.i += 1

		return identifier

	def parseLiteral(self):
		while self.input[self.i] in self.WHITESPACE: self.i += 1  # advance through whitespace

		literal = ''
		while self.input[self.i] not in (self.WHITESPACE + [self.COMMA] + [self.CLOSELIST] + [self.CLOSEOBJECT]):
			literal += self.input[self.i]
			self.i += 1

		if self.input[self.i] == self.COMMA:
			self.i -= 1

		if literal.lower() == 'null':
			return None

		elif literal.lower() == 'true':
			return True

		elif literal.lower() == 'false':
			return False

		elif '.' in literal:
			return float(literal)

		else:
			return int(literal)

	@staticmethod
	def printObject(obj, indent=0):
		TAB = '   '
		for k in obj.keys():
			print('{0}{1}:'.format(TAB * indent, k))
			if type(obj[k]) is dict:
				JsonParser.printObject(obj[k], indent + 1)
			else:
				print('{0}{1}'.format(TAB * (indent + 1), obj[k]))
