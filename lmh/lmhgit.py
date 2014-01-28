#!/usr/bin/env python

"""
This is the entry point for the Local Math Hub utility. 

.. argparse::
   :module: lmhgit
   :func: create_parser
   :prog: lmhgit

"""

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
import glob
import argparse
from subprocess import call

from . import lmhutil

def create_parser():
  parser = argparse.ArgumentParser(description='Local MathHub Git Wrapper.')
  add_parser_args(parser)
  return parser

def add_parser(subparsers):
  parser_status = subparsers.add_parser('git', formatter_class=argparse.RawTextHelpFormatter, help='run git command on multiple repositories')
  add_parser_args(parser_status)

def add_parser_args(parser):
  parser.add_argument('cmd', nargs=1, help="a git command to be run.")
  parser.add_argument('--all', "-a", default=False, const=True, action="store_const", help="runs a git command on all repositories currently in lmh")
  parser.add_argument('repository', type=lmhutil.parseRepo, nargs='*', help="a list of repositories for which to run the git command.").completer = lmhutil.autocomplete_mathhub_repository
  parser.epilog = """
Repository names allow using the wildcard '*' to match any repository. It allows relative paths. 
  Example:  
    */*       - would match all repositories from all groups. 
    mygroup/* - would match all repositories from group mygroup
    .         - would be equivalent to "git status ."
""";

def do_git(rep, cmd):
  print "doing git {cmd} on {rep}".format(cmd=cmd, rep=rep)
  cmd_lst = [lmhutil.which("git")];
  cmd_lst.extend(cmd.split(" "))
  call(cmd_lst, cwd=rep);

def do(args):
  if len(args.repository) == 0:
    args.repository = [lmhutil.tryRepo(".", lmhutil.lmh_root()+"/MathHub/*/*")]
  if args.all:
    args.repository = [lmhutil.tryRepo(lmhutil.lmh_root()+"/MathHub", lmhutil.lmh_root()+"/MathHub")]  

  for repo in args.repository:
    for rep in glob.glob(repo):
      do_git(rep, args.cmd[0]);
      
