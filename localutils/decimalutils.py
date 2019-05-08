def parse(decimalinput):
	if decimalinput is None:
		return None
	try:
		ret = int(float(decimalinput) * 10000) / 10000
		return ret
	except:
		return None

def truncate(floatinput: float, precision: int = 2):
	ret = int(floatinput * (10**precision))
	return float(ret) / (10**precision)