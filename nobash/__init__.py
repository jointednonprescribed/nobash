#!/usr/bin/env python3
__all__ = []
__version__ = '1.0'
# Pre-init modules:
#  * 'exc'
#---------------------

import os, sys, subprocess, time

# import pre-init module 'exc'
from . import exc


# Application error-stamping class

class AppStamp: # {
	__slots__ = ('__appstamp__', '__pappstamp__')

	def __init__(self, name, *, print_stamp:bool=True): # {
		## Application label ("appstamp") for error messages
		self.__appstamp__  = name
		## Whether or not to print the appstamp
		self.__pappstamp__ = True
	# }

	def toggle_visiblity(self):
		self.__pappstamp__ = not self.__pappstamp__
	def set_visibility(self, visibility:bool=True):
		self.__pappstamp__ = visibility
	def get(self):
		return self.__appstamp__
	def set(self, newstamp):
		self.__appstamp__ = newstamp

	## Print an error message with or without app stamp.
	def perror(self, *a, **kw): # {
		if kw['file'] == None:
			kw['file'] = sys.stderr
		if self.__pappstamp__:
			print(self.__appstamp__ + ':', *a, **kw)
		else:
			print(*a, **kw)
	# }
	## Return error string with or without appstamp instead of printing
	def serror(self, *a): # {
		if self.__pappstamp__:
			errstr = f'{self.__appstamp__}: {a[0]}'
		else:
			errstr = a[0]

		for arg in a[1:]:
			errstr = f'{errstr} {arg}'

		return errstr
	# }
	stamp = serror
# }
_appstamp = AppStamp('nobash')
_perror    = lambda *a, **kw: _appstamp.perror(*a, **kw)
_serror    = lambda *a: _appstamp.serror(*a)
_stamp     = lambda *a: _appstamp.stamp(*a)


# Standard Package Utilites

## Get all of the directories and files in a directory.
def ls(basedir: str, *, recursive:bool=False, print=None, filter=None, as_tuple:bool=False): # {
	from . import path
	if not isinstance(basedir, str):
		basedir = str(basedir)
	if not os.path.exists(basedir):
		raise exc.PathnameError(_serror(f'Pathname \'{basedir}\' doesn\'t exist.'))

	if basedir.find('~') >= 0:
		basedir = os.path.expanduser(basedir)

	if os.path.isfile(basedir):
		return [basedir]
	elif not os.path.isdir(basedir):
		raise exc.PathnameError(_serror(f'Pathname \'{basedir}\' is neither directory nor file.'))

	if filter == None:
		filter = lambda *a, **kw: True
	elif not hasattr(filter, '__call__'):
		raise exc.ArgumentError(_serror('Cannot accept \'filter\' keyword parameter of non-function type.'))

	paths = []
	for path in os.listdir(basedir):
		if filter(path):
			paths.append(path)

	if as_tuple:
		return tuple(paths)
	else:
		return paths
# }

## Execute a subprocess application
execsp = lambda *a,**kw: subprocess.Popen(*a, **kw)

class ScriptEntryPoint: # {
	__slots__ = ('__starttime__', '__basedir__', '__basefile__', '__cwd__', '__args__')

	def __init__(self, appstamp: AppStamp | None = None, *, print_runtime:bool=False, **kw): # {
		if __name__ != '__main__':
			raise RuntimeError(_serror("Cannot fetch script entry point unless running as __main__."))
		basefile           = os.path.abspath(sys.argv[0])
		self.__basedir__   = os.path.dirname(basefile)
		self.__basefile__  = basefile
		self.__cwd__       = os.getcwd()
		self.__args__      = sys.argv[1:]
		self.__starttime__ = time.time_ns()
		self.__pruntime__  = print_runtime
	# }
	def __del__(self): # {
		t = time.time_ns()

		from . import time

		if self.__pruntime__:
			print(f'Entry point closed after {time.Time(t - self.__starttime__)!s}')

		super().__del__()
	# }

	def __str__(self): # {
		return f"{super().__str__()[:-1]}\n\t: Running script '{self.__basefile__}'>"
	# }
	def __repr__(self): # {
		return self.__str__()
	# }
# }
entry_point = lambda *a, **kw: ScriptEntryPoint(*a, **kw)

