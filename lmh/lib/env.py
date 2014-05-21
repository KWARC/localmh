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
import sys
import os.path

from lmh.lib.io import std


from subprocess import Popen

"""Installation directory of lmh"""
install_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/../../")

"""Data directory of lmh"""
data_dir = os.path.realpath(install_dir + "/MathHub")

"""Excternale dependencies directory of lmh"""
ext_dir = os.path.realpath(install_dir + "/ext")

def which(program):
	"""Returns the full path to program similar to the *nix command which"""
	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
	
	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return None

"""sTex directory"""
stexstydir = install_dir+"/ext/sTeX/sty"

"""LatexML directory"""
latexmlstydir = install_dir+"/ext/sTeX/LaTeXML/lib/LaTeXML/texmf"


#
# Perl 5 etc
#

"""The perl5 root directories"""
perl5root = [install_dir+"/ext/perl5lib/", os.path.expanduser("~/")]

"""Perl5 binary directories"""
perl5bindir = ":".join([p5r+"bin" for p5r in perl5root])+":"+install_dir+"/ext/LaTeXML/bin"+":"+install_dir+"/ext/LaTeXMLs/bin"

"""Perl5 lib directories"""
perl5libdir = ":".join([p5r+"lib/perl5" for p5r in perl5root])+":"+install_dir+"/ext/LaTeXML/blib/lib"+":"+install_dir+"/ext/LaTeXMLs/blib/lib"

def perl5env(_env = {}):
	"""perl 5 environment generator"""
	_env["PATH"]=perl5bindir+":"+_env["PATH"]
	try:
		_env["PERL5LIB"] = perl5libdir+":"+ _env["PERL5LIB"]
	except:
		_env["PERL5LIB"] = perl5libdir
		_env["STEXSTYDIR"] = stexstydir
	return _env


def run_shell(shell = None):
	"""Runs a shell that is ready for any perl5 things"""
	if shell == None:
		shell = os.environ["SHELL"] or which("bash")
	else:
		shell = util.which(shell)
		if shell == None:
			shell = args.shell

	# Make a perl 5 environment
	_env = perl5env(os.environ)

	try:
		runner = Popen([shell], env=_env, cwd=install_dir, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
	except:
		# we could not find that
		return 127

	def do_the_run():
		try:
			runner.wait()
		except KeyboardInterrupt:
			runner.send_signal(signal.SIGINT)
			do_the_run()

	std("Opening a shell ready to compile for you. ")
	do_the_run()

	return runner.returncode