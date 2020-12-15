from newick import read
import sys
import json

glottonames = json.loads(open('glottonames.json').read())
ilis = json.loads(open('ilis.json').read())
codelevels = {}
for g in glottonames:
    codelevels[glottonames[g][0]] = f"g{glottonames[g][1]}"

def sanitized_name(n):
    parts = n.name[1:-1].split(" [")
    name = parts[0]
    code = parts[1][:-1]
    return (name, code)

def index_status(name, code):
    if name in ilis:
        if name in glottonames:
            if code == glottonames[name][0]: #good match
                return r'\flaggedgood'
        return r'\flaggedmid' #potential mismatch
    return ''

def tikz(node, out, level=0):
    outputname, outputcode  = sanitized_name(node)
    indentation = level * ' '
    option = f"\\{codelevels.get(outputcode,'')}, "
    option +=  index_status(outputname, outputcode)
    out.write("%s[\\namecode{%s}{%s}, %s\n" % (indentation, outputname, outputcode, option))
    for subnode in node.descendants:
        tikz(subnode, out, level=level+1)
    out.write(f"{indentation}]\n")

def write_tikz(tree, filename):
    with open(f"treetex/{filename}.tex", 'w') as out:
        out.write(textemplate[0])
        tikz(tree, out)
        out.write(textemplate[1])

textemplate = (r"""\documentclass{standalone}
\usepackage[linguistics,edges]{forest}
\usepackage{libertine}
\input{definitions.tex}
\begin{document}
\tiny
\begin{forest} for tree={grow'=east,
                           delay={where content={}{shape=coordinate}{}},
                           },
               forked edges,
""",
r"""\end{forest}
\end{document}
""")



if __name__ == "__main__":
    offset = 9999999
    #offset = 4
    trees = read('newick_nodistance.txt')
    for tree in trees[:offset]:
        filename =  sanitized_name(tree)[1]
        print(filename)
        if filename in ("atla1278","aust1307","indo1319", "sino1245","afro1255"):
            for i, subtree in enumerate(tree.descendants):
                subfilename =  f"{filename}-{i+1}"
                print(subfilename)
                if subfilename in ("atla1278-5","aust1307-3","indo1319-1"):
                    for j, subsubtree in enumerate(subtree.descendants):
                        subsubfilename =  f"{filename}-{i+1}.{j+1}"
                        print(subsubfilename)
                        write_tikz(subsubtree, subsubfilename)
                else:
                        write_tikz(subtree, subfilename)
        else:
            write_tikz(tree, filename)

