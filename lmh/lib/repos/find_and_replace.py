import os
import re
from string import Template

from lmh.lib.io import is_string
from lmh.lib.io import find_files, std, err, read_file, write_file
from lmh.lib.dirs import lmh_locate
from lmh.lib.repos.local import find_repo_dir, match_repo

def find_and_replace_file(file, match, replace, replace_match = None):
    """Finds and replaces a single file. """

    if len(match) != len(replace):
        err("Find and Replace patterns are not of the same length. ")
        return False

    # Compile thex regexp
    try:
        match_regex = [re.compile(m) for m in match]
    except Exception as e:
        err(e)
        err("Unable to compile regular expressions. ")
        return False

    # get the repository
    repo = os.path.relpath(find_repo_dir(file), lmh_locate("content"))

    # We did nothing yet
    did = False
    if replace_match == None:
        def replace_match(match, replace):
            # TODO: Migrate this to the parent scope.
            # did = True

            # Make a template,
            replacer_template = {}
            replacer_template["repo"] = repo
            for i, g in enumerate(match.groups()):
                replacer_template["g"+str(i)] = g

            # And replace in it
            return Template(replace).substitute(replacer_template)

    # Read file and search
    file_content = read_file(file)
    new_file_content = file_content

    # Iterate over the regexes and replace
    for (m, r) in zip(match_regex, replace):
        new_file_content = re.sub(m, lambda x:replace_match(x, r), new_file_content)

    if file_content != new_file_content:
        std(file)
        # If something has changed, write back the file.
        write_file(file, new_file_content)
    if did:
        std(file)
    return did

def find_file(file, match):
    """Finds inside a single file. """

    # Compile thex regexp
    try:
        match_regex = [re.compile(m) for m in match]
    except Exception as e:
        err(e)
        err("Unable to compile regular expressions. ")
        return False

    # Read file and search
    file_content = read_file(file)

    ret = False
    for i, m in enumerate(match_regex):
        if re.search(m, file_content) != None:
            if len(match) > 1:
                std(str(i), file)
            else:
                std(file)
            ret = True

    return ret


def find_cached(files, match, replace = None, replace_match = None):
    """Finds and replaces inside of files. """

    # Make sure match and replace are arrays
    match = [match] if is_string(match) else match
    if replace != None:
        replace = [replace] if is_string(replace) else replace

        if len(replace) != len(match):
            err("Find and Replace patterns are not of the same length. ")
            return False


    rep = False
    for file in files:
        repo = os.path.relpath(find_repo_dir(file), lmh_locate("content"))
        matcher = [Template(m).substitute(repo=repo) for m in match]
        if replace != None:
            rep = find_and_replace_file(file, matcher, replace, replace_match = replace_match) or rep
        else:
            rep = find_file(file, matcher) or rep
    return rep

def find(rep, args):
    """Finds pattern in repositories"""

    match = args.matcher
    replace = args.replace[0] if args.apply else None

    # Find files in the repository
    files = find_files(match_repo(rep, abs=True), "tex")[0]

    return find_cached(files, match, replace)
