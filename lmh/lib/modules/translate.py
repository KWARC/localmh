import re
import json

from lmh.lib.modules.symbols import add_symbols

import lmh.lib.io
from lmh.lib.io import read_file, write_file, std, err

def create_multi(modname, pre_terms, *langs):
    if len(langs) == 0:
        err("You need to create at least one language. ")
        return False
    lang = langs[0]

    # Read the module
    try:
        content = read_file(modname+".tex")
    except:
        err("Unable to read original module", modname+".tex")
        return False

    # Module content
    module_content_regex = r"^((?:.|\n)*)\\begin\{module\}\[(?:(.*),\s*)?id=([^,\]]*)(?:\s*(.*))\]((?:.|\n)*?)\\end\{module\}((?:.|\n)*)$"
    module_move_regex = r"(\\(?:gimport|symdef|symtest|symvariant|symi+)(?:(?:\[(?:[^\]])*\])|(?:\{(?:[^\}])*\}))*((\n|$|\s)?))"

    # Find the module
    mod_content = re.findall(module_content_regex, content)

    if len(mod_content) != 1:
        err("Expected exactly one module environment. (Is the module really monolingual?)")
        return False

    mod_content = mod_content[0]

    # Main Language Content
    main_module = ""
    main_language = ""

    # Prefix and suffix to add to the module
    mod_prefix = mod_content[0]
    mod_suffix = mod_content[5]

    # Id of the module
    mod_id = mod_content[2]
    mod_meta = mod_content[1]+mod_content[3]
    if mod_meta != "":
        mod_meta = "["+mod_meta+"]"

    # We only want to move these
    module_to_move = "".join([m[0] for m in re.findall(module_move_regex, mod_content[4])])
    module_keep = re.sub(module_move_regex, lambda match:match.group(2), mod_content[4])

    # Assemble the main module
    main_module = mod_prefix
    main_module += "\\begin{modsig}"+mod_meta+"{"+mod_id+"}"
    main_module += module_to_move
    main_module += "\\end{modsig}"
    main_module += mod_suffix

    try:
        write_file(modname+".tex", main_module)
    except:
        err("Unable to write", modname+".tex")
        return False

    # Assemble the main language binding
    main_language = mod_prefix
    main_language += "\\begin{modnl}"+mod_meta+"{"+mod_id+"}{"+lang+"}\n"
    main_language += module_keep
    main_language += "\n\\end{modnl}"
    main_language += mod_suffix

    try:
        write_file(modname+"."+lang+".tex", main_language)
    except:
        err("Unable to write", modname+"."+lang+".tex")
        return False

    lmh.lib.io.__supressStd__ = True

    # Add the symbols frome the language file name
    add_symbols(modname+"."+lang+".tex")

    # Translate to all the other languages
    for l in langs[1:]:
        if not transmod(modname, lang, l, pre_terms = pre_terms):
            lmh.lib.io.__supressStd__ = False
            return False
    lmh.lib.io.__supressStd__ = False

    std("Created multilingual module", modname+".tex")

    # Thats it.
    return True



def transmod(modname, org_lang, dest_lang, pre_terms = {}):
    """Translate a module from one language to another. """

    # Load json from a file if pre_terms is a string
    if type(pre_terms) == str:
        try:
            pre_terms = json.loads(read_file(pre_terms))
        except:
            try:
                pre_terms = json.loads(pre_terms)
            except:
                err("Unable to load json in file %r" % pre_terms)
                err("Make sure you have given a valid JSON-encoded string or path to a valid .json file. ")
                return False

    # Load the set of pre-translated terms
    if org_lang in pre_terms:
        pre_terms = pre_terms[org_lang]
        if dest_lang in pre_terms:
            pre_terms = pre_terms[dest_lang]
        else:
            pre_terms = {}
    else:
        pre_terms = {}


    # filenames for the original + translated modules
    orfn = "%s.%s.tex" % (modname, org_lang)
    newfn = "%s.%s.tex" % (modname, dest_lang)

    # read the original file
    try:
        content = read_file(orfn)
    except:
        err("Unable to read original module", orfn)
        return False

    #
    # STEP 1: Replace the third argument to the modnl + viewnl environments
    #

    content = re.sub(r"(\\begin\{modnl\}\[[^\]]*\]\{[^\}]*\})\{"+org_lang+r"\}", r"\1{"+dest_lang+"}", content)
    content = re.sub(r"(\\begin\{viewnl\}\[[^\]]*\]\{[^\}]*\})\{"+org_lang+r"\}", r"\1{"+dest_lang+"}", content)

    #
    # STEP 2: Update everything inside the environments
    #

    def replacer(match):
        content = match.group(2)

        # trefi -> mtrefi
        content = re.sub(r"\\trefi\[([^\]]*)\]\{([^\}]*)\}", r"\\mtrefi[\1?\2]{\\ttl{\2}}", content)
        # trefii -> mtrefii
        content = re.sub(r"\\trefii\[([^\]]*)\]\{([^\}]*)\}\{([^\}]*)\}", r"\\mtrefii[\1?\2-\3]{\\ttl{\2 \3}}", content)
        # trefiii -> mtrefiii
        content = re.sub(r"\\trefiii\[([^\]]*)\]\{([^\}]*)\}\{([^\}]*)\}\{([^\}]*)\}", r"\\mtrefiii[\1?\2-\3-\4]{\\ttl{\2 \3 \4}}", content)

        # defi
        content = re.sub(r"\\defi\[([^\]]*)\]\{([^\}]*)\}", r"\\defi[\1]{\\ttl{\2}}", content)
        content = re.sub(r"\\defi\{([^\}]*)\}", r"\\defi[\1]{\\ttl{\1}}", content)
        # defii
        content = re.sub(r"\\defii\[([^\]]*)\]\{([^\}]*)\}\{([^\}]*)\}", r"\\defii[\1]{\\ttl{\2}}{\\ttl{\3}}", content)
        content = re.sub(r"\\defii\{([^\}]*)\}\{([^\}]*)\}", r"\\defii[\1-\2]{\\ttl{\1}}{\\ttl{\2}}", content)
        # defiii
        content = re.sub(r"\\defiii\[([^\]]*)\]\{([^\}]*)\}\{([^\}]*)\}\{([^\}]*)\}", r"\\defiii[\1]{\\ttl{\2}}{\\ttl{\3}}{\\ttl{\4}}", content)
        content = re.sub(r"\\defiii\{([^\}]*)\}\{([^\}]*)\}\{([^\}]*)\}", r"\\defiii[\1-\2-\3]{\\ttl{\1}}{\\ttl{\2}}{\\ttl{\3}}", content)


        def inner_supper(m):
            # Inner replacement function
            # Inserts the \ttl before any trailing whitespace.

            (sub_inner, n) = re.subn(r"([\n\f\t\v\s]+)$", r"}\1", m.group(1))
            if n == 0:
                sub_inner+="}"

            return r"\ttl{"+sub_inner+m.group(6)

        def supper(m):
            # Outer replacement function.
            toreplace = m.group(4)

            if re.match(r"^([\n\f\t\v\s]*)$", toreplace):
                # we are only whitespaces => do nothing
                pass
            else:
                # we are ntop only whitespaces => replace some sentences.
                toreplace = re.sub(r"(((\w)+\s+)*((\w)+\s*))([\.\!\?\,\;]?)", inner_supper, toreplace)
            return m.group(1)+toreplace+m.group(5)

        # Replace non-wrapped text fragments
        content = re.sub(r"((\]|\}|\$[^\$]*\$)(\w*))([^\\\{\}\$\]\[]+)(\s*)", supper, content)

        # and return the content
        return match.group(1)+content+match.group(4)

    # Replace text inside the environments of modnl and viewnl
    content = re.sub(r"(\\begin{modnl})((.|\n)*)(\\end{modnl})", replacer, content)
    content = re.sub(r"(\\begin{viewnl})((.|\n)*)(\\end{viewnl})", replacer, content)

    #
    # STEP 3: Apply the pre-translated directory to \ttl{...}
    #

    # Replace all the technical terms
    def replacer2(match):
        # prefer full matches
        if match.groups(1)[0] in pre_terms:
            return match.groups(1)[0][pre_terms]


        # Split the terms and look check if we can translate them
        terms = []
        for t in match.groups(1)[0].split(" "):
            if t in pre_terms:
                terms.append((pre_terms[t], True))
            else:
                terms.append((t, False))

        # Put the results back together
        result = ""
        is_open_ttl = False

        # For each of the terms
        for (r, s) in terms:
            if not is_open_ttl:
                # We do not have an openn ttl
                if s:
                    result+=r+" "
                else:
                    result+="\\ttl{"+r+" "
                    is_open_ttl = True
            else:
                # We do have an open ttl
                if s:
                    result += result[:-1]+"} "+r+" "
                    is_open_ttl = False
                else:
                    result += r+" "
        # Close the last bracket if needed
        result = result[:-1]
        if is_open_ttl:
            result +="}"

        return result

    content = re.sub(r"\\ttl\{([^\}]*)\}", replacer2, content)

    # write back the file
    try:
        write_file(newfn, content)
    except:
        err("Unable to write new module", newfn)
        return False

    # and do some logging
    std("Prepared translation of", modname, "from")
    std(orfn)
    std("to")
    std(newfn)
    std("Please finish the translation and then commit the module. ")

    # we need it for the return code
    return True
