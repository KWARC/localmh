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

from lmh.lib.io import err
from lmh.lib.modules.translate import create_multi

from . import CommandClass

class Command(CommandClass):
    def __init__(self):
        self.help="Create a new multilingual module from a monlingual one"
    def add_parser_args(self, parser):
        parser.add_argument('source', nargs=1, help="Name of the existing module. ")
        parser.add_argument('dest', nargs="+", help="Name(s) of the new language(s). ")
        parser.add_argument('--terms', default=None, help="Terms to pre-translate. Either a Path to a json file or a JSON-encoded string. ")

        parser.epilog = """
Example: lmh multiling mono.tex en de

Which creates a new multilingual module mono.tex with languages
mono.en.tex and mono.de.tex

The terms argument should have the following structure:

{
    "source_language": {
        "target_language": {
            "word": "translation"
        }
    }
}


Will require manual completion of the translations. """

    def do(self, args, unknown_args):
        args.source = args.source[0]

        if not os.path.isfile(args.source) or not args.source.endswith(".tex"):
            err("Module", args.source, "does not exist or is not a valid module. ")

        # Remove the .tex
        args.source = args.source[:-len(".tex")]

        return create_multi(args.source, args.terms, *args.dest)
