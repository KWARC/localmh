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

import argparse
import lmh.lib.about

def create_parser():
  parser = argparse.ArgumentParser(description='Local MathHub About information. ')
  add_parser_args(parser)
  return parser

def add_parser(subparsers, name="about"):
  about_parser = subparsers.add_parser(name, formatter_class=argparse.RawTextHelpFormatter, help='shows version and general information. ')
  add_parser_args(about_parser)

def add_parser_args(parser):
  pass

def do(args):
  print("LMH, Version " + lmh.lib.about.version)
  print("")
  print(lmh.lib.about.license)