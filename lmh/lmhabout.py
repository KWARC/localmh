#!/usr/bin/env python

"""
This is the entry point for the Local Math Hub utility. 

.. argparse::
   :module: lmhabout
   :func: create_parser
   :prog: lmhabout

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
import re
import glob
import argparse
import subprocess
import pkg_resources


from . import lmhutil

def create_parser():
  parser = argparse.ArgumentParser(description='Local MathHub About information. ')
  add_parser_args(parser)
  return parser

def add_parser(subparsers):
  about_parser = subparsers.add_parser('about', formatter_class=argparse.RawTextHelpFormatter, help='shows version and general information. ')
  add_parser_args(about_parser)

def add_parser_args(parser):
  parser.add_argument('--version', "-v", default=False, const=True, action="store_const", help="show version and exit")
  parser.add_argument('--license', "-l", default=False, const=True, action="store_const", help="show license and exit")

def do(args):
  if args.license:
    print """
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """
  else:
    try:
      print pkg_resources.require("lmh")[0].version, " (via pip)"
    except pkg_resources.DistributionNotFound:
      print "local (unversioned)"
