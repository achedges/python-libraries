def gcd(a: int, b: int) -> int:
	if a == 0: return b
	if b == 0: return a
	
	divisor: int = a if a < b else b
	dividend: int = b if a < b else a
	remainder: int = int(dividend % divisor)
	
	return gcd(divisor, remainder)
