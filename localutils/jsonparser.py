class JsonToken:

	def __init__(self, token: str, text: str):
		self.token = token
		self.text = text

	def __repr__(self):
		return '{0} ({1})'.format(self.token, self.text)

class JsonParser:

	def __init__(self, jsonstring: str):
		self.input = jsonstring.strip()
		self.n = len(self.input)
		self.i = 0
		self.result = dict()

		self.__stream = None


	def __nextToken(self) -> JsonToken:
		self.i += 1
		if self.i < len(self.__stream):
			return self.__stream[self.i]
		else:
			return JsonToken('EOF', 'EOF')


	def parse(self):
		self.__stream = self.__tokenizeInput()
		self.i = 0

		if self.__stream[0].token != '{':
			raise Exception("JSON documents must start with '{'")

		self.result = self.__parseObject()
		return self.result


	def __parseObject(self):
		obj = {}

		key = self.__nextToken()

		while key.token != '}':

			if key.token == ',':
				key = self.__nextToken()

			separator = self.__nextToken()
			value = self.__nextToken()

			if key.token != 'ID':
				raise Exception('Invalid object key: {0}'.format(key.token))
			if separator.token != ':':
				raise Exception('Invalid key-value separator: {0}'.format(separator.token))

			if value.token == '{':
				obj[key.text] = self.__parseObject()
			elif value.token == '[':
				obj[key.text] = self.__parseList()
			elif value.token == 'ID':
				obj[key.text] = value.text
			elif value.token == 'LIT':
				obj[key.text] = JsonParser.__parseLiteral(value.text)

			key = self.__nextToken()

		return obj


	def __parseList(self):
		lst = []
		token = self.__nextToken()
		while token.token != ']':
			if token.token == 'ID':
				lst.append(token.text)
			elif token.token == 'LIT':
				lst.append(JsonParser.__parseLiteral(token.text))
			elif token.token == '{':
				lst.append(self.__parseObject())
			elif token.token == '[':
				lst.append(self.__parseList())

			token = self.__nextToken()

		return lst


	@staticmethod
	def __parseLiteral(text):
		if text == 'true':
			return True
		elif text == 'false':
			return False
		elif text == 'null':
			return None
		elif '.' in text:
			return float(text)
		else:
			return int(text)


	def __tokenizeInput(self):

		_WS = [ ' ', '\t', '\n', '\r' ]
		_TK = [ '{', '}', '[', ']', ',', ':' ]
		tokenstream = []

		while self.i < self.n:
			if self.input[self.i] in _WS:
				self.i += 1
				continue

			if self.input[self.i] in _TK:
				tokenstream.append(JsonToken(self.input[self.i], self.input[self.i]))

			elif self.input[self.i] == '"':
				_id = ''
				self.i += 1
				while self.i < self.n:
					if self.input[self.i] == '"' and self.input[self.i-1] != '\\':
						break

					if self.input[self.i] == '"' and self.input[self.i-1] == '\\':
						_id[-1] = '"' # double-quotes are escaped, so replace the backslash
					else:
						_id += self.input[self.i]

					self.i += 1

				tokenstream.append(JsonToken('ID', _id))

			else:
				_lit = self.input[self.i]
				self.i += 1
				while self.i < self.n:
					if self.input[self.i] in [ ',', ']', '}' ]:
						self.i -= 1 # back-up so we can capture the ending token in the stream
						break
					elif self.input[self.i] not in _WS:
						_lit += self.input[self.i]

					self.i += 1

				tokenstream.append(JsonToken('LIT', _lit))

			self.i += 1

		return tokenstream
