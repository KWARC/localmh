"""
generic input / output functions used by lmh
"""

import sys
import os
import os.path
import shutil
import getpass

from subprocess import Popen, PIPE

def is_string(s):
    """
    Checks if an object is a string
    """
    try:
        return isinstance(s, basestring)
    except NameError:
        return isinstance(s, str)

def term_colors(c):
    """
    Returns terminal encoding for a color given by a string
    """

    colors = {
            "grey": "\033[01;30m",
            "red": "\033[01;31m",
            "green": "\033[01;32m",
            "yellow": "\033[01;33m",
            "blue": "\033[01;34m",
            "magenta": "\033[01;35m",
            "cyan": "\033[01;36m",
            "white": "\033[01;37m",
            "normal": "\033[00m"
    }

    from lmh.lib.config import get_config

    if get_config("self::colors"):
        return colors[c]
    else:
        return ""


#
# Error & Normal Output
#

# Allow supression of outputs
__supressStd__ = False
__supressErr__ = False
__supressIn__ = False

def std(*args, **kwargs):
    """
    Prints text to stderr. Supports keyword argument newline (to add or not add
    a newline at the end. )
    """

    newline = True

    # allow only the newline kwarg
    for k in kwargs:
        if k != "newline":
            raise TypeError("std() got an unexpected keyword argument '"+k+"'")
        else:
            newline = kwargs["newline"]

    text = " ".join([str(text) for text in args]) + ('\n' if newline else '')

    if not __supressStd__:
        sys.stdout.write(text)

def err(*args, **kwargs):
    """
    Prints text to stderr (in red). Supports keyword arguments newline (add a
    newline at the end) and colors (supress the color).
    """

    newline = True
    colors = True

    # allow only the newline kwarg
    for k in kwargs:
        if k != "newline" and k != "colors":
            raise TypeError("err() got an unexpected keyword argument '"+k+"'")
        else:
            try:
                newline = kwargs["newline"]
            except:
                pass
            try:
                colors = kwargs["colors"]
            except:
                pass

    if not __supressErr__:
        text = " ".join([str(text) for text in args]) + ('\n' if newline else '')
        if colors:
            sys.stderr.write(term_colors("red")+text+term_colors("normal"))
        else:
            sys.stderr.write(text)

def std_paged(*args, **kwargs):
    """
    Pages output if a pager is available.
    """

    from lmh.lib.config import get_config

    newline = True

    # allow only the newline kwarg
    for k in kwargs:
        if k != "newline":
            raise TypeError("std() got an unexpected keyword argument '"+k+"'")
        else:
            newline = kwargs["newline"]

    if not __supressStd__:
        pager = get_config("env::pager")

        if pager == "":
            return std(*args, **kwargs)
        try:
            p = Popen([pager], stdout=sys.stdout, stderr=sys.stderr, stdin=PIPE)
            p.communicate(" ".join([str(text) for text in args]) + ('\n' if newline else ''))
        except:
            err("Unable to run configured page. ")
            err("Please check your value for env::pager. ")
            err("Falling back to STDOUT. ")
            return std(*args, **kwargs)


def read_raw(query = None, hidden = False):
    """
    Reads a line of text form stdin
    """

    if __supressIn__:
        err("Interactivity disabled, aborting. ")
        os._exit(1)
    if query != None:
        std(query, newline=False)
    sys.stdout.flush()# Make sure all the output is here
    if hidden:
        return getpass.getpass("").strip()
    else:
        return sys.stdin.readline().strip()

#
# File reading / writing
#

def write_file(filename, text):
    """
    Writes text to a file
    """

    # Write the text to file
    text_file = open(filename, "w", encoding="utf8")

    if is_string(text):
        text_file.write(text)
    else:
        text_file.write("\n".join(text) + "\n")
    text_file.close()

    return True

def read_file(filename):
    """
    Reads text from a file
    """

    # Read some text and then close the file
    text_file = open(filename, "r", encoding="utf8")

    try:
        text = text_file.read()
        text_file.close()
    except UnicodeDecodeError:
        text_file = open(filename, "r", encoding="latin-1")
        text = text_file.read()
        text_file.close()

    return text

def read_file_lines(filename = None):
    """
    Reads all lines from a file. If not file is given stdin will be used.
    """

    if filename == None:
        return sys.stdin.readlines()

    # Read lines and then close the file

    # Read some text and then close the file
    text_file = open(filename, "r", encoding="utf8")

    try:
        lines = text_file.readlines()
        text_file.close()
    except UnicodeDecodeError:
        text_file = open(filename, "r", encoding="latin-1")
        lines = text_file.readlines()
        text_file.close()

    return [l.rstrip('\n') for l in lines]

def copytree(src, dst, symlinks=False, ignore=None):
    """
    Replacement for shutil.copytree
    """

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def find_files(directory, *ext):
    """
    Finds all files with given extensions i a given direcory recursively
    """
    res = []

    ext = ["."+e for e in ext]
    res = [[] for e in ext]

    for root, dirs, files in os.walk(directory):
        for file in files:
            for (i, e) in enumerate(ext):
                if file.endswith(e):
                    res[i].append(os.path.join(root, file))
    return tuple(res)


#
# EASTERGG
# wrapped in try catch so as not to cause any trouble
# entirely undocumented
#
try:
    import lolcat
    import argparse
    import random
    import datetime


    loloptions = {
        "spread": 3.0,
        "freq": 0.1,
        "seed": 0,
        "animate": False,
        "force": False,
        "os": random.randint(0, 256)
    }

    loloptions = argparse.Namespace(**loloptions)

    def lol_write(text):
        from lmh.lib.config import get_config
        if get_config("self::colors") and get_config("::eastereggs"):
            a = lolcat.LolCat(mode = lolcat.detect_mode())
            a.cat([text], loloptions)
            loloptions.os += len(text.split("\n"))
            lolcat.reset()
            return
        sys.__stdout__.write(text)

    now = datetime.datetime.now()
    if now.month == 4 and now.day == 1:
        sys.stdout = {
                "write": lambda x:lol_write(x),
                "flush": lambda:True
        }

        sys.stdout = argparse.Namespace(**sys.stdout)
except:
    pass
