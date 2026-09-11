"""Parse a .mia file with the draft grammar and print the tree.

strict=True makes Lark fail on any shift/reduce conflict or overlapping
regex terminals, so a clean build means the grammar is unambiguous LALR(1).
"""
import pprint

from crunge.mia import assets

from crunge.mia.compile.parse.parser import parse
from crunge.mia.compile.ast.nodes import to_json

if __name__ == "__main__":
    src = assets.load("blox.mia").read()

    ast = parse(src)
    json = to_json(ast)
    pprint.pprint(json)
