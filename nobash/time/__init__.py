#!/usr/bin/env python3

import os, sys, subprocess, time

from . import exc
from .. import _serror


# THE FOLLOWING CLASS ('Time') WAS TAKEN AND SLIGHTLY MODIFIED FROM 'stopwatch'
# (https://github.com/jointednonprescribed/stopwatch)
# 'stopwatch' is released under the GNU GPL v3.0, so thereby
# requirements of that license, the 'nobash' project itself
# will be released under the terms of the GNU GPL v3.0.
class Time: # {
	unit_order = ('ns', 'us', 'ms', 's', 'm', 'hrs')

	__slots__ = (*unit_order, 'time_totals')

	def __init__(self, arg0: int | dict | tuple): # {
		if isinstance(arg0, int):
			ns = arg0
			self.ns = ns
			ns //= 1000
			self.us = ns
			ns //= 1000
			self.ms = ns
			ns //= 1000
			self.s  = ns
			ns //= 60
			self.m  = ns
			ns //= 60
			self.hrs = ns

			time_totals = {'hrs': ns}
			if ns > 0:
				biggest = 5
			else:
				biggest = None
			arg0 -= ns * 3600000000000 # hrs to ns

			# These code blocks first convert from ns to various larger units of
			# time by floor dividing, then they multiply by the susame factor to
			# calculate the REAL number of nanoseconds inside of that many of
			# that unit of time to get the remainder in nanoseconds.
			ns = arg0 // 60000000000 # ns to mins
			time_totals['m'] = ns
			if biggest == None and ns > 0:
				biggest = 4
			arg0 -= ns * 60000000000 # mins to ns

			ns = arg0 // 1000000000 # ns to s
			time_totals['s'] = ns
			if biggest == None and ns > 0:
				biggest = 3
			arg0 -= ns * 1000000000 # s to ns

			ns = arg0 // 1000000 # ns to ms
			time_totals['ms'] = ns
			if biggest == None and ns > 0:
				biggest = 2
			arg0 -= ns * 1000000 # ms to ns

			ns = arg0 // 1000 # ns to us
			time_totals['us'] = ns
			if biggest == None and ns > 0:
				biggest = 1
			arg0 -= ns * 1000 # us to ns

			# the final remainder in nanoseconds
			time_totals['ns'] = arg0
			if biggest == None:
				time_totals['largest'] = 0
			else:
				time_totals['largest'] = biggest

			self.time_totals = time_totals
		elif isinstance(arg0, dict):
			l = len(Time.unit_order)
			hr      = arg0['hrs']
			if not isinstance(hr, int) or hr < 0:
				raise TypeError(_serror("Entry for keys 'hrs', 'm', 's', 'ms', 'us', 'ns' must be an unsigned int."))
			m       = arg0['m']
			if not isinstance(m, int) or m < 0:
				raise TypeError(_serror("Entry for keys 'hrs', 'm', 's', 'ms', 'us', 'ns' must be an unsigned int."))
			s       = arg0['s']
			if not isinstance(s, int) or s < 0:
				raise TypeError(_serror("Entry for keys 'hrs', 'm', 's', 'ms', 'us', 'ns' must be an unsigned int."))
			ms      = arg0['ms']
			if not isinstance(ms, int) or ms < 0:
				raise TypeError(_serror("Entry for keys 'hrs', 'm', 's', 'ms', 'us', 'ns' must be an unsigned int."))
			us      = arg0['us']
			if not isinstance(us, int) or us < 0:
				raise TypeError(_serror("Entry for keys 'hrs', 'm', 's', 'ms', 'us', 'ns' must be an unsigned int."))
			ns      = arg0['ns']
			if not isinstance(ns, int) or ns < 0:
				raise TypeError(_serror("Entry for keys 'hrs', 'm', 's', 'ms', 'us', 'ns' must be an unsigned int."))
			largest = arg0['largest']
			if not isinstance(largest, int):
				raise TypeError(_serror(f"Entry for key 'largest' must be an int from 0-{(l-1)!s}."))
			elif largest < 0 or largest >= l:
				raise IndexError(_serror(f"Entry for key 'largest' must be an int from 0-{(l-1)!s}."))
			
			time_totals = {
				'hrs': hr,
				'm':  m,
				's':  s,
				'ms': ms,
				'us': us,
				'ns': ns,
				'largest': largest
			}
			self.time_totals = time_totals

			ns = time_totals['ns']
			self.ns  = ns
			self.us  = ns // 1000
			self.ms  = ns // 1000000
			self.s   = ns // 1000000000
			self.m   = ns // 60000000000
			self.hrs = ns // 3600000000000
		elif isinstance(arg0, tuple):
			l0 = len(arg0)
			l1 = len(Time.unit_order)
			if l0 < 0 or l0 >= l1:
				raise exc.IterableLengthError(_serror(f'Length of input argument must be 0-{(l1-1)!s}.'))

			units = list(arg0)
			if l0 < (l1-1):
				units = [*units, *(unit for unit in arg0)]

			time_totals = {}
			time_totals['hrs'] = units[5]
			if units[5] > 0:
				biggest = 5
			else:
				biggest = None
			time_totals['m']  = units[4]
			if biggest == None and units[4] > 0:
				biggest = 4
			time_totals['s']  = units[3]
			if biggest == None and units[3] > 0:
				biggest = 3
			time_totals['ms'] = units[2]
			if biggest == None and units[2] > 0:
				biggest = 2
			time_totals['us'] = units[1]
			if biggest == None and units[1] > 0:
				biggest = 1
			time_totals['ns'] = units[0]
			ns = units[0]
			if biggest == None:
				biggest = 0

			time_totals['largest'] = biggest

			self.ns  = ns
			self.us  = ns // 1000
			self.ms  = ns // 1000000
			self.s   = ns // 1000000000
			self.m   = ns // 60000000000
			self.hrs = ns // 3600000000000
	# }

	def __int__(self): # {
		return self.ns
	# }
	def __float__(self): # {
		return float(self.ns)
	# }
	def __tuple__(self): # {
		return (self.ns, self.us, self.ms, self.s, self.m, self.hr)
	# }
	def __dict__(self): # {
		return self.time_totals
	# }
	def __getitem__(self, index): # {
		if isinstance(index, int):
			l = len(Time.unit_order)
			if index < 0 or index >= l:
				raise OverflowError(_serror(f'Index argument {index!s} is out of bounds (0-{(l-1)!s}).'))
			else:
				return Time.unit_order[index]
		elif isinstance(index, str):
			return self.time_totals[index]
		else:
			raise IndexError(_serror('Only acceptable types for subscript are \'int\' and \'str\'.'))
	# }
	def __setitem__(self, *a): # {
		raise Exception(_serror('Cannot set item values for this object.'))
	# }
	def __str__(self): # {
		big1 = self.time_totals['largest']
		if big1 > 1:
			big  = big1, big1 - 1, big1 - 2
		elif big1 > 0:
			big  = big1, big1 - 1
		else:
			big  = (big1,)
		bign = len(big)

		unit = Time.unit_order[big[0]]
		str = f"{self.time_totals[unit]!s}{unit}"
		if bign > 1:
			i = 1
			for unit in big[1:]:
				unit = Time.unit_order[big[i]]
				str  = f"{str} {self.time_totals[unit]!s}{unit}"
				i += 1

		return str
	# }
	def __repr__(self): # {
		return self.__str__()
	# }

	@classmethod
	def timed_command(cls, *cmd, **kw): # {
		proc = None
		start = None
		end = None

		gettime = time.time_ns

		start = gettime()
		proc = subprocess.Popen(*cmd, **kw)
		proc.wait()
		end = gettime()

		return Time(end - start)
	# }
# }

