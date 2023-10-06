"""

This script looks for a __version__.py containing a VERSION var to increment
The third value [2] will be incremented by one

This would normally be called by a git pre commit hook and then
the version file would be staged by by the pre commit hook

"""

from ast import literal_eval as make_tuple

import logging
logging.basicConfig()
logger = logging.getLogger()

import os

logger.info("Looking for __version__.py")

try:
	index = 0
	data = ""
	found = False
	with open('__version__.py', 'r') as f:
		logger.info("found __version__.py, looking for VERSION")
		data = f.readlines()
		for idx, line in enumerate(data):
			if "VERSION" in line:
				index = idx
				found = True
				break
	if found:
		tokens = data[index].split("=")
		newVersion = make_tuple(tokens[-1].strip())
		lst = list(newVersion)
		lst[-1] += 1
		newVersion = tuple(lst)
		newLine = "VERSION = " + str(newVersion)+"\n"
		data[index] = newLine
		with open('__version__.py', 'w') as f:
			f.writelines(data)
	else:
		logging.warning("VERSION not found")
except ImportError:
	logger.warning("__version__.py not found, not incrementing")