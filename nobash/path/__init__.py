#!/usr/bin/env python3

import os

from contextlib import contextmanager

from .. import exc, _serror


# Resolve, between multiple given pathnames, what the common root path of all
# of them is.
def resolve_pathroot(*roots): # {
	pass
# }
# Inflate a pathname that contains special characters ('.', '..', '~', '*'),
# or contains shell environment variables.
def inflate_path(path: str, *, filter=lambda *a,**kw: True, return_root=False): # {
	if not isinstance(path, str):
		path = str(path)

	# expand environment variables, '.', '..', and '~', all that is left is '*'.
	path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))

	startidx = path.find('*')
	if startidx < 0:
		return path

	snippet = path[:startidx]

	isdir   = path[startidx+1] == os.sep
	nextidx = path[startidx+1:].find('*')
	recurse = nextidx >= 0

	results = []

	i = 0
	for dirpath, dirnames, filenames in os.walk(snippet):
		if i == 0:
			i += 1
			continue

		# WRITE PSEUDO CODE AND CONTINUE IMPLEMENTATION!

		i += 1

	if return_root:
		return (snippet, results)
	else:
		return results
# }
def inflate_paths(*paths, return_root=False): # {
	paths = []
	if return_root:
		roots = []

	root    = None
	infpath = None

	for path in paths: # {
		if not isinstance(path, str):
			path = str(path)
		inflated = inflate_path(path, return_root=return_root)
		if return_root:
			root, infpath = inflated
			roots.append(root)
		else:
			infpath = inflated
		if isinstance(infpath, list):
			paths = [*paths, *infpath]
		else:
			paths = [*paths, infpath]
	# }

	if return_root:
		return (resolve_pathroot(*roots), paths)
	else:
		return paths
# }

# Declare this method now as it is needed for compilation of the Path class,
# it will eventually be implemented as __new__ for PathSelection.
fselect = lambda *a, **kw: None
class Path: # {
	__slots__ = ('_pathname', '__levelcount')

	# If this path is to a directory, this function will return _pathname,
	# otherwise, if it is a file, the directory containing that file will
	# be returned.
	def get_dir(self): # {
		# NEEDS IMPLEMENTATION
		pass
	# }
	# Get the containing directory of this object referenced by _pathname
	def get_containing_dir(self): # {
		# NEEDS IMPLEMENTATION
		pass
	# }

	def __init__(self, path, **kwargs): # {
		path = os.path.expanduser(os.path.expandvars(path))

		if os.path.isabs(path):
			self._pathname = path
		else:
			self._pathname = os.path.abspath(path)

		self.__levelcount = self._pathname.count(os.sep)
	# }
	def __new__(cls, path, *a, **kw): # {
		if isinstance(path, str) and path.find('*') >= 0:
			return fselect(path, *a, **kw)
		else:
			return super().__new__(path, **kw)
	# }
	__resolve_root__ = get_dir

	def __str__(self):
		return self._pathname
	def __repr__(self):
		return self._pathname
# }
class PathSelection: # {

	def selection(self, *, filter=None): # {
		# Generate with iselection()
		for i, path in self.iselection(filter=filter):
			yield path
	# }
	def iselection(self, *, filter=None): # {
		if filter == None:
			filter = lambda path, **kw: True
		elif not hasattr(filter, '__call__'):
			raise exc.ArgumentError(_serror('Cannot accept \'filter\' keyword parameter of non-function type.'))

		# NEEDS IMPLEMENTATION!
		pass
	# }
	def files(self, *, filter=None): # {
		if filter == None:
			use_filter = os.path.isfile
		else:
			use_filter = lambda file, **kw: os.path.isfile(file) and filter(file)

		# Generate with iselection()
		for i, path in self.iselection(filter=use_filter):
			yield path
	# }
	def ifiles(self, *, filter=None): # {
		if filter == None:
			use_filter = os.path.isfile
		else:
			use_filter = lambda file, **kw: os.path.isfile(file) and filter(file)

		# Generate with iselection()
		for i, path in self.iselection(filter=use_filter):
			yield (i, path)
	# }
	def dirs(self, *, filter=None): # {
		if filter == None:
			use_filter = os.path.isdir
		else:
			use_filter = lambda path, **kw: os.path.isdir(path) and filter(path)

		# Generate with iselection()
		for i, path in self.iselection(filter=use_filter):
			yield path
	# }
	def idirs(self, *, filter=None): # {
		if filter == None:
			use_filter = os.path.isdir
		else:
			use_filter = lambda path, **kw: os.path.isdir(path) and filter(path)

		# Generate with iselection()
		for i, path in self.iselection(filter=use_filter):
			yield (i, path)
	# }

	def contains(self, find_path, filter=None): # {
		for i, path in self.iselection(filter=filter):
			if path == find_path:
				return True

		return False
	# }

	def get_paths_listed(self, *, filter=None): # {
		paths = []

		for i, path in self.iselection(filter=filter):
			paths.append(path)

		return paths
	# }
	def get_files_listed(self, *, filter=None): # {
		files = []
		if filter == None:
			use_filter = os.path.isfile
		else:
			use_filter = lambda file, **kw: os.path.isfile(file) and filter(file)

		for i, path in self.iselection(filter=use_filter):
			files.append(path)

		return files
	# }
	def get_dirs_listed(self, *, filter=None): # {
		dirs = []
		if filter == None:
			use_filter = os.path.isdir
		else:
			use_filter = lambda path, **kw: os.path.isdir(path) and filter(path)

		for i, path in self.iselection(filter=use_filter):
			dirs.append(path)

		return dirs
	# }
	def get_paths(self, **kw): # {
		return tuple(self.get_paths_listed(**kw))
	# }
	def get_files(self, **kw): # {
		return tuple(self.get_files_listed(**kw))
	# }
	def get_dirs(self, **kw): # {
		return tuple(self.get_dirs_listed(**kw))
	# }
	def get_path_count(self, **kw): # {
		return tuple(self.get_paths_listed(**kw))
	# }
	def get_file_count(self, **kw): # {
		try:
			kwfilter = kw['filter']
		except IndexError:
			kwfilter = None

		if kwfilter == None:
			filter = lambda file, **kw: os.path.isfile(file)
		else:
			if not hasattr(filter, '__call__'):
				raise exc.ArgumentError(_serror('Cannot accept \'filter\' keyword parameter of non-function type.'))
			else:
				filter = lambda path, **kw: os.path.isfile(path) and kwfilter(path)
		i = 0
		for i, path in self.iselection(filter=filter):
			pass

		return i + 1
	# }
	def get_dir_count(self, **kw): # {
		try:
			kwfilter = kw['filter']
		except IndexError:
			kwfilter = None

		if kwfilter == None:
			filter = lambda path, **kw: os.path.isdir(path)
		else:
			if not hasattr(filter, '__call__'):
				raise exc.ArgumentError(_serror('Cannot accept \'filter\' keyword parameter of non-function type.'))
			else:
				filter = lambda path, **kw: os.path.isdir(path) and kwfilter(path)
		i = 0
		for i, path in self.iselection(filter=filter):
			pass

		return i + 1
	# }

	def add_paths(self, *paths, filter=None): # {
		if filter == None:
			filter = lambda *a, **kw: True
		elif not hasattr(filter, '__call__'):
			raise exc.ArgumentError(_serror('Cannot accept \'filter\' keyword parameter of non-function type.'))

		pathroot, inflated = inflate_paths(*paths, return_root=True)

		root = resolve_pathroot(self._root, pathroot)
		if root - self.root != 0:
			oldroot = self._root
			self._root = root
		else:
			oldroot = None

		i=0
		for path in inflated:
			# NEEDS IMPLEMENTATION
			i+=1

		# Return the amount of paths added to the selection.
		return i
	# }
	def remove_paths(self, *paths, filter=None): # {
		if filter == None:
			filter = lambda *a, **kw: True
		elif not hasattr(filter, '__call__'):
			raise exc.ArgumentError(_serror('Cannot accept \'filter\' keyword parameter of non-function type.'))

		# NEEDS IMPLEMENTATION
		return
	# }
	def clear_selection(self): # {
		self._selection = {}
	# }

	def resolve_root(self): # {
		pass
	# }
	__resolve_root__ = resolve_root
	# Recheck the common root of all the selected paths and refactor the
	# selection.
	def reset_root(self): # {
		pass
	# }

	def __init__(self, *paths, **kwargs): # {
		self.build = lambda *a,**kw: None

		self._root = None
		self._selection = {}
		self.add_paths(*paths)
	# }
	def __init__(self): # {
		self.build = lambda *a,**kw: None

		self._root = None
		self._selection = {}
	# }

	def __tuple__(self):
		return self.get_paths()
	def __list__(self):
		return self.get_paths_listed()
	def __int__(self):
		return self.get_path_count()
	def __dict__(self):
		return dict(self._selection)
	def __str__(self):
		return str(self._selection)
	def __repr__(self):
		return str(self._selection)

	def builder(self, func): # {
		if not isinstance(func, type(enumerate)) and not hasattr(func, '__call__'):
			raise exc.ArgumentError(_serror('Builder must be a generator function or other callable object.'))
		else:
			self.build = func
	# }
# }
fselect = lambda *a,**kw: PathSelection(*a, **kw)

