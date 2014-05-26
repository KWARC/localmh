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

from lmh.lib.env import which
from lmh.lib.io import std, read_raw
from lmh.lib.about import version
from lmh.lib.config import get_config, set_config

def init():
	if get_config("state::lastversion") == version:
		# First run is done
		return

	# First run
	first_run()
	set_config("state::lastversion", version)

def q_program(pgr):

	res = read_raw("Where is the "+pgr+" executable? Leave blank to autodetect at runtime. >")
	if res != "":
		res = which(res)
		std("Using", pgr, "at", res)
		set_config("env::"+pgr, res)

def first_run():
	std("Welcome to lmh. ")
	std("This seems to be the first time you are running this version of lmh. ")
	std("This setup routine will automatically run and help you configure lmh automatically. ")

	if read_raw("Do you wish to continue? hit enter to continue or enter s to skip. ") != "":
		std("Skipping setup. ")
		return

	res = ""
	while not res in ["y", "n"]:
		res = read_raw("Do you want to enable output colors[y/n]? >").lower()

	if res == "y":
		std("Colors enabled. ")
		set_config("self::enable_colors", "true")

	res = ""
	while not res in ["y", "n"]:
		res = read_raw("Do you want to use a pager to page long outputs[y/n]? >").lower()

	if res == "y":
		try:
			res = ""
			while which(res) == None:
				res = read_raw("Which pager do you want to use (How about less)? >")

			res = which(res)

			std("Using pager:", res)
			set_config("env::pager", res)

		except KeyboardInterrupt:
			std("Not using any pager. ")

	q_program("git")
	q_program("svn")
	q_program("pdflatex")
	q_program("perl")
	q_program("cpanm")
	q_program("make")
	q_program("tar")

	res = ""
	while not res in ["y", "n"]:
		res = read_raw("Do you want to re-run this setup for future versions[y/n]? >").lower()

	if res == "n":
		std("Setup disabled for future versions. ")
		set_config("self::showfirstrun", False)

	read_raw("Setup complete. Press enter to continue. ")