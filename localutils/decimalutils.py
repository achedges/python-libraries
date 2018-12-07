def parse(decimalinput):
	if decimalinput is None:
		return None
	try:
		ret = int(float(decimalinput) * 10000) / 10000
		return ret
	except:
		return None