from enum import Enum
from time import sleep


class ThreadWaitMultiplier(Enum):
	Fixed = 1
	Exponential = 2

class ThreadWait:

	def __init__(self, initialMilliseconds: float=100, multiplier: ThreadWaitMultiplier=ThreadWaitMultiplier.Exponential):
		self.initialWaitSeconds: float = initialMilliseconds / 1000 # sleep() operates on seconds
		self.waitSeconds: float = self.initialWaitSeconds
		self.multiplier: ThreadWaitMultiplier = multiplier

	def waitnext(self) -> None:
		sleep(self.waitSeconds)
		self.waitSeconds *= self.multiplier.value
		return

	def reset(self) -> None:
		self.waitSeconds = self.initialWaitSeconds
		return
