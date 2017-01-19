"""
Main file for gliffyDb

GliffyDB is intended to help make sense of DB structures by generating a visual
representation of the schema in a format compatible with the free Gliffy app.

The most time-consuming part is extracting the DB data into a usable format
that allows for easy 'linking' to show relationships between tables.

This will automatically scan & generate column object groups for each table,
where each column is in it's own separate 'object', allowing very precise
mapping to be done between tables.

This not only helps provide a 'birds-eye view' of the DB as a whole, but is
also very useful when attempting to decipher stored procedures as you can
simply take copies of the relevant tables and then draw out the relationships
defined in the stored procedure.
"""

# Standard Library
from pprint import PrettyPrinter
import json
# Third Party
# Local
from gliffy.gliffy import Gliffy
from utils.dump import dump

pp = PrettyPrinter()

if __name__ == '__main__':
    print('testing out this sucker')
    g = Gliffy()  # type: Gliffy

    grp = g.group()
    txt = g.line()

    print('\n\n')
    pp.pprint(str(g.text()))
    print('\n\n')
    pp.pprint(str(g.rectangle()))
    print('\n\n')
    pp.pprint(str(g.line()))
    print('\n\n')
