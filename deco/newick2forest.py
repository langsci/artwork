from newick import read
import sys

def sanitized_name(node):
    parts = node.name[1:-1].split(" [")
    name = parts[0]
    code = parts[1][:-1]
    return (name, code)


def tikz(node, out, level=0):
    outputname, outputcode  = sanitized_name(node)
    indentation = level * ' '
    out.write("{%s}[\\namecode{%s}{%s}" % (indentation, outputname, outputcode))
    for subnode in node.descendants:
        tikz(subnode, out, level=level+1)
    out.write(f"{indentation}]")


textemplate = (r"""\documentclass{standalone}
\usepackage[linguistics,edges]{forest}
\usepackage{libertine}
\forestset{
  every leaf node/.style={
    if n children=0{#1}{}
  }
}
\input{definitions.tex}
\begin{document}
\tiny
\begin{forest} for tree={grow'=east,
                           delay={where content={}{shape=coordinate}{}},
                           every leaf node={rounded corners=2pt, draw, fill=black!5}
                           },
               forked edges,
""",
r"""\end{forest}
\end{document}
""")

if __name__ == "__main__":
    offset = 9999999
    trees = read('newick_nodistance.txt')
    for tree in trees[:offset]:
        filename =  sanitized_name(tree)[1]
        with open(f"treetex/{filename}.tex", 'w') as out:
            out.write(textemplate[0])
            tikz(tree, out)
            out.write(textemplate[1])
