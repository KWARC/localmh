"""
This file is part of LMH.

LMH is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LMH is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LMH.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import re
import sys
import shutil

from lmh.lib import reduce
from lmh.lib.io import find_files, std, err
from lmh.lib.env import data_dir

from lmh.lib.repos.local import match_repos
from lmh.lib.repos.find_and_replace import find_cached

def movemod(source, dest, modules, simulate = False):
	"""Moves modules from source to dest. """

	# change directory to MathHub root, makes paths easier
	if simulate:
		std("cd "+data_dir)
	else:
		os.chdir(data_dir)

	finds = []
	replaces = []

	odest = dest

	for module in modules:

		dest = odest

		# Figure out the full path to the source
		srcpath = source + "/source/" +  module

		# Assemble source paths further
		srcargs = (source + "/" + module).split("/")
		srcapath = "/".join(srcargs[:-1])
		srcbpath = srcargs[-1]

		# Assemble all the commands
		oldcall = "\[" + srcapath + "\]\{"+srcbpath+"\}"
		oldcall_long = "\[(.*)repos=" + srcapath + "(.*)\]\{"+srcbpath+"\}"
		oldcall_local = "\{"+srcbpath+ "\}"
		newcall = "[" + dest + "]{"+srcbpath+"}"
		newcall_long = "[$g1" + dest + "$g2]{"+srcbpath+"}"

		dest += "/source/"

		file_patterns = ["", ".de", ".en"]

		# Move the files
		if simulate:
			for pat in file_patterns:
				std("mv "+srcpath + pat +".tex"+ " "+ dest + " 2>/dev/null || true")
		else:
			for pat in file_patterns:
				# try to move the file if it exists
				try:
					shutil.move(srcpath + pat + ".tex", dest)
				except:
					pass

		def run_lmh_find(find, replace):
			finds.append(find)
			replaces.append(replace)

		# Run all the commands
		m = "("+"|".join(["gimport", "guse", "gadopt"])+")"
		run_lmh_find(r'\\'+m+oldcall, '\\$g0'+newcall)
		run_lmh_find(r'\\'+m+oldcall_local, '\\$g0'+newcall)

		m = "("+ "|".join(["importmhmodule", "usemhmodule", "adoptmhmodule", "usemhvocab"]) + ")"
		run_lmh_find(r'\\'+m+oldcall_long, '\\$g0'+newcall_long)
		run_lmh_find(r'\\'+m+oldcall_local, '\\$g0'+newcall_long)

	for f in finds:
		std(f)

	files = reduce([find_files(r, "tex")[0] for r in match_repos(data_dir, abs=True)])

	return find_cached(files, finds, replace=replaces)
