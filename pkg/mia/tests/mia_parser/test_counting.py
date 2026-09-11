"""Parse a .mia file with the draft grammar and print the tree.

strict=True makes Lark fail on any shift/reduce conflict or overlapping
regex terminals, so a clean build means the grammar is unambiguous LALR(1).
"""

from crunge.mia import assets
from crunge.mia.compile.parse.parser import parse_raw

if __name__ == "__main__":
    src = assets.load("counting.mia").read()

    if not src.endswith("\n"):
        src += "\n"
    print(parse_raw(src).pretty())
