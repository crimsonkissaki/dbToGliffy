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
# Third Party
# Local
from gliffy.gliffy import Gliffy
from utils.dump import dump
from utils import util
from gliffy import entity, graphic

ppr = PrettyPrinter()
pp = ppr.pprint

# if you declare a positional argument & kwargs you can provide the positional argument in the kwargs

"""
make table
    - set table name
        - use this css
    - add columns
        - use this css


"""


class GliffyDB(object):

    gliffy = Gliffy()

    def make_table(self):
        """
        Makes the JSON to represent a DB table in Gliffy

        :return:
        """

        # make group
        # make container rect
        # make table name rect
        # make table name text
        # for each col
        #   make col name rect
        #   make col name text

        grp = self.gliffy.make_group()
        cont = self.gliffy.make_rectangle()

        grp.add_child(cont)

        return grp

    def get_table_name(self):
        return 'DAC_DMS_DEFINITION'

    def get_table_cols(self, table=None):
        return ('ID', 'DMS_TYPE', 'DMS_PROVIDER_ID', 'DMS_DEFINITION_DESCRIPTION', 'CREATED_BY',
                      'CREATED_TIMESTAMP', 'UPDATED_BY', 'UPDATED_TIMESTAMP')

    def set_table_name(self):
        pass

    def add_columns(self):
        pass


def test_make():
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


def test():
    g = Gliffy()  # type: Gliffy
    var = g.make_group()
    # test_table()
    print('\n\n')
    dump(var)
    print('\n\n')
    print(var)
    print('\n\n')


def t2(*args):
    for k, v in args:
        print('k = {}, v = {}'.format(k, v))


if __name__ == '__main__':
    g = Gliffy()
    grp = g.make_group()
    g.add_to_stage(grp)

    rect = g.make_rectangle()
    grp.add_child(rect)

    txt = g.make_text({'text': 'Testing 123'})
    rect.add_child(txt)

    var = g.to_json()

    print('\n\n')
    print('STAGE:')
    dump(rect)
    print('\n\n')
    print(rect.to_json())
    print('\n\n')

