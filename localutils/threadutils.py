from time import sleep


class ThreadWait:
	def __init__(self, resolution=.1, initialWait=1, increment=2):
		self.resolution = resolution
		self.waitval = initialWait
		self.increment = increment # 1=linear, 2=exponential

	def waitnext(self):
		sleep(self.resolution * self.waitval)
		self.waitval *= self.increment
		return