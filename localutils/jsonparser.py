from typing import Any, Dict, List, Optional, TypeVar, Union

class JsonToken:

	def __init__(self, token: str, text: str):
		self.token = token
		self.text = text

	def __repr__(self):
		return '{0} ({1})'.format(self.token, self.text)


class JsonParser:
	
	T = TypeVar('T')

	def __init__(self, jsonstring: str):
		self.input = jsonstring.strip()
		self.n = len(self.input)
		self.i = 0
		self.result: Optional[Union[List[Any], Dict[str, Any]]] = None
		self.__stream = []


	def parse(self) -> Optional[Union[List[Any], Dict[str, Any]]]:
		self.__tokenizeInput()
		self.i = 0

		if self.__stream[0].token == '{':
			self.result = self.__parseObject()

		elif self.__stream[0].token == '[':
			self.result = self.__parseList()

		else:
			self.result = None

		return self.result
	
	
	def parseToType(self, userType: T) -> Optional[T]:
		self.parse()
		if self.result is None:
			return None

		return JsonParser.__parseUserType(self.result, userType)
	
	
	@staticmethod
	def __parseUserType(resultobj: Union[List[Any], Dict[str, Any]], userType: T) -> Optional[Union[List[Any], T]]:
		if not isinstance(resultobj, list) and not isinstance(resultobj, dict):
			return None
		
		if isinstance(resultobj, list):
			return resultobj # if the parsed result is a list, there's no way to know which elements of the list should be instances 'T'
		
		t = userType()
		for key in resultobj:
			if hasattr(t, key):
				attr = getattr(t, key)
				if isinstance(resultobj[key], dict) and not isinstance(attr, dict): # if parsed JSON element is a dict, but the member attr is not
					setattr(t, key, JsonParser.__parseUserType(resultobj[key], type(attr)))
				else:
					setattr(t, key, resultobj[key])
				
		return t


	def __tokenizeInput(self):

		_WS = [ ' ', '\t', '\n', '\r' ]
		_TK = [ '{', '}', '[', ']', ',', ':' ]

		while self.input[self.i] not in [ '{', '[' ]:
			self.i += 1 # advance to the first open brace/bracket
			if self.i <= self.n:
				break

		while self.i < self.n:
			if self.input[self.i] in _WS:
				self.i += 1
				continue

			if self.input[self.i] in _TK:
				self.__stream.append(JsonToken(self.input[self.i], self.input[self.i]))

			elif self.input[self.i] == '"':
				_id = []
				self.i += 1
				while self.i < self.n:
					if self.input[self.i] == '"' and self.input[self.i-1] != '\\':
						break

					if self.input[self.i] == '"' and self.input[self.i-1] == '\\':
						_id[-1] = '"' # double-quotes are escaped, so replace the backslash
					else:
						_id.append(self.input[self.i])

					self.i += 1

				self.__stream.append(JsonToken('ID', ''.join(_id)))

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

				self.__stream.append(JsonToken('LIT', _lit))

			self.i += 1

		return


	def __nextToken(self) -> JsonToken:
		self.i += 1
		if self.i < len(self.__stream):
			return self.__stream[self.i]
		else:
			return JsonToken('EOF', 'EOF')


	@staticmethod
	def __parseLiteral(text) -> Any:
		if text == 'true':
			return True
		elif text == 'false':
			return False
		elif text == 'null':
			return None
		elif '.' in text or 'e' in text:
			return float(text)
		else:
			return int(text)


	def __parseList(self) -> List[Any]:
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
			if token.token == 'EOF':
				break

		return lst


	def __parseObject(self) -> Dict[str, Any]:
		obj = {}

		key = self.__nextToken()

		while key.token != '}':

			if key.token == ',':
				key = self.__nextToken()

			separator = self.__nextToken()
			value = self.__nextToken()

			if key.token != 'ID':
				raise Exception('Invalid token detected for object key: {0}'.format(key.token))
			if separator.token != ':':
				raise Exception('Invalid token detected for key-value separator: {0}'.format(separator.token))

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


	@staticmethod
	def serializeJsonObject(json: Union[dict, list], noformat:bool=False) -> str:
		if type(json) is dict:
			return JsonParser.__serializeObject(json, 0 if noformat else 1)
		
		elif type(json) is list:
			return JsonParser.__serializeList(json, 0 if noformat else 1)
		
		else:
			raise Exception('JSON serializer needs an object input')


	@staticmethod
	def __serializeObject(obj: dict, indent:int=0) -> str:
		ret = ['{']

		if indent > 0:
			ret.append('\n')

		keys = list(obj.keys())
		for i in range(len(keys)):
			ret.append('{0}"{1}": {2}'.format('\t' * indent, keys[i], JsonParser.__serializeValue(obj[keys[i]], indent)))

			if i < len(keys) - 1:
				ret.append(',')

			if indent > 0:
				ret.append('\n')

		ret.append('{0}}}'.format('\t' * (indent-1)))
		return ''.join(ret)


	@staticmethod
	def __serializeList(lst: list, indent:int=0) -> str:
		ret = ['[']
		length: int = len(lst)
		i: int = 0

		if indent > 0:
			ret.append('\n')

		for item in lst:
			ret.append('\t' * indent)
			ret.append(JsonParser.__serializeValue(item, indent))

			if i < length - 1:
				ret.append(',')

			if indent > 0:
				ret.append('\n')
				
			i += 1

		ret.append('{0}]'.format('\t' * (indent-1)))
		return ''.join(ret)


	@staticmethod
	def __serializeValue(value, indent:int=0) -> str:
		if type(value) is dict:
			return JsonParser.__serializeObject(value, indent+1 if indent > 0 else indent)
		elif type(value) is list or type(value) is set:
			return JsonParser.__serializeList(value, indent+1 if indent > 0 else indent)
		elif type(value) is str:
			return '"{0}"'.format(value)
		elif type(value) is bool:
			return 'true' if value else 'false'
		elif value is None:
			return 'null'
		else:
			return str(value)
