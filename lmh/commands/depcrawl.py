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

from lmh.lib.io import err
from lmh.lib.repos.local import calc_deps

from . import CommandClass

class Command(CommandClass):
    def __init__(self):
        self.help="Crawl current repository for dependencies"
    def add_parser_args(self, parser):
        parser.add_argument('--apply', metavar='apply', const=True, default=False, action="store_const", help="Writes found dependencies to MANIFEST.MF")
    def do(self, args, unknown):
        res = calc_deps(args.apply)
        if res:
            return True
        else:
            err("lmh depcrawl must be run from within a Repository. ")
            return False
