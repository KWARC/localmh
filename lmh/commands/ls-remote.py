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

from lmh.lib import helper
from lmh.lib.io import std, term_colors
from lmh.lib.repos import is_installed
from lmh.lib.repos.remote import ls_remote
from lmh.lib.help import repo_wildcard_remote

def add_parser(subparsers, name="ls-remote"):
    parser_status = subparsers.add_parser(name, formatter_class=helper.LMHFormatter, help='list remote repositories')
    add_parser_args(parser_status)


def add_parser_args(parser):
    parser.add_argument('spec', nargs='*', help="list of repository specefiers. ")
    parser.epilog = repo_wildcard_remote

def do(args):
    res = ls_remote(*args.spec)
    if res == False:
        return False
    else:
        for r in res:
            if is_installed(r):
                std(term_colors("green")+r+term_colors("normal"))
            else:
                std(term_colors("red")+r+term_colors("normal"))
        return True
