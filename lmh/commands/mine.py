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

import os.path

from lmh.lib.repos.local import export, restore

from . import CommandClass

class Command(CommandClass):
    def __init__(self):
        self.help="Manage all locally installed repositories"
    def add_parser_args(self, parser):
        group = parser.add_mutually_exclusive_group()

        group.add_argument("--export", dest="dump_action", action="store_const", const=0, default=0, help="Dump list of installed repositories in file. ")
        group.add_argument("--import", dest="dump_action", action="store_const", const=1, help="Install repositories listed in file. ")

        parser.add_argument("file", nargs="?", help="File to use. If not given, assume STDIN or STDOUT respectivelsy. ")
    def do(self, args, unknown):
        if args.dump_action == 0:
            # Export
            if not args.file:
                #Print them to stdout
                return export()
            else:
                #Put them in a file
                return export(os.path.abspath(args.file[0]))
        else:
            if not args.file:
                #Read frm stdin
                return restore()
            else:
                #Read from file
                return restore(os.path.abspath(args.file[0]))
