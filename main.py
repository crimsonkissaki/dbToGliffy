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

ppr = PrettyPrinter()
pp = ppr.pprint

if __name__ == '__main__':
    g = Gliffy()  # type: Gliffy

    '''
    c = g.make('constraint', kind='startConstraint')
    print('\n\n')
    dump(c)
    print('\n\n')
    pp(c)
    print('\n\n')
    '''

    tomake = ['group', 'rectangle', 'text', 'line', 'constraint']
    print('\n\n')
    for m in tomake:
        if m == 'constraint':
            t = g.make(m, kind='startConstraint')
        else:
            t = g.make(m)
        print('Making {}'.format(m))
        dump(t)
        print('\n\n')
        print(t)
        print('\n\n')
