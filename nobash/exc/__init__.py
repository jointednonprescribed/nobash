#!/usr/bin/env python3
# This module is to be loaded before __init__.py of root package (pre-init).


# Exception types

## "Report this to the Developer" error
class ReportToDevError(Exception): # {
	def __init__(self, *a, **kw):
		super(*a, **kw)
# }

## Iterable of unexpected length (too short or long)
class IterableLengthError(Exception): # {
	def __init__(self, *a, **kw):
		super().__init__(*a, **kw)
# }

## Error with an argument that was passed to a function
class ArgumentError(Exception): # {
	def __init__(self, *a, **kw):
		super(*a, **kw)
# }

## Error with a given path string
class PathnameError(Exception): # {
	def __init__(self, *a, **kw):
		super(*a, **kw)
# }

