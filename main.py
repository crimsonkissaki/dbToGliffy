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
from collections import OrderedDict
# Third Party
# Local
from gliffy.gliffy import Gliffy
from utils.dump import dump
from utils import util
from gliffy import graphics, entities

ppr = PrettyPrinter()
pp = ppr.pprint

# if you declare a positional argument & kwargs you can provide the positional argument in the kwargs


class GliffyDB(object):

    tn_cell_style = {'strokeWidth': 1, 'strokeColor': '#000000'}
    tn_text_style = {'text': '', 'css': {'font-size': '14px', 'font-family': 'Courier', 'bold': True}}
    cn_cell_style = {'strokeWidth': 1, 'strokeColor': '#cccccc'}
    cn_text_style = {'text': '', 'css': {'font-size': '12px', 'font-family': 'Courier'}}

    g = Gliffy()

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

        #grp = self.g.group()
        #self.g.add(grp)
        cont = self.g.rectangle({'strokeColor': '#000000', 'fillColor': 'none'})
        # grp.add_child(cont)
        self.g.add(cont)

        '''
        tnts = self.tn_text_style.copy()
        tnts['text'] = self.get_table_name()
        tn = self.make_cell(self.tn_cell_style, tnts)
        cont.add_child(tn)

        cols = self.get_table_cols()
        cnts = self.cn_text_style.copy()
        for col in cols:
            cnts['text'] = col
            cn = self.make_cell(self.cn_cell_style, cnts)
            cont.add_child(cn)
        '''

        return str(self.g)

    def get_table_name(self):
        return 'DAC_DMS_DEFINITION'

    def get_table_cols(self, table=None):
        return ('ID', 'DMS_TYPE', 'DMS_PROVIDER_ID', 'DMS_DEFINITION_DESCRIPTION', 'CREATED_BY',
                      'CREATED_TIMESTAMP', 'UPDATED_BY', 'UPDATED_TIMESTAMP')

    def make_cell(self, cell_props, text_props):
        r = self.g.rectangle(cell_props)
        t = self.g.text(text_props)
        r.add_child(t)

        return r


def save_to_file(data):
    f = open('output.gliffy', 'w')
    f.write(data)
    f.close()


def blah():
    one = 'oops'
    two = 'blarg'

    return one, two


if __name__ == '__main__':
    # test()
    # gdb = GliffyDB()
    # save_to_file(gdb.make_table())
    # graphic.Text.default_family = 'Helvetica'

    a = {'a': 'a.a', 'b': 'a.b'}
    b = {'a': 'b.a'}
    a['a'] = b.get('a', 'default')
    a['b'] = b.get('b', a['b'])

    print('\n\n')
    print(a)
    print('\n\n')

    '''
    tn_css = {'strokeWidth': 1, 'strokeColor': '#000000'}
    tn_text_css = {'text': 'table name', 'css': {'font-size': '14px', 'font-family': 'Courier', 'bold': True}}
    cn_css = {'strokeWidth': 1, 'strokeColor': '#cccccc'}
    cn_text_css = {'text': 'column name', 'css': {'font-size': '12px', 'font-family': 'Courier'}}

    g = Gliffy()
    grp = g.group()
    rect = g.rectangle({'fillColor': 'none'})
    grp.add_child(rect)

    txt = g.text(tn_text_css)
    grp.add_child(txt)

    rect2 = g.rectangle(cn_css)

    g.add([grp, rect2])

    print('\n\n')
    dump(g.stage)
    print('\n\n')

    save_to_file(str(g))
    '''

    '''
    t = graphic.Text()
    tprops = {'color': '123456789', 'font-family': 'Wingdings', 'bold': 'TrUe', 'italic': 'bork', 'paddingTop': '3', }
    t.validate_properties(tprops)
    print('\n\n', 'props now:', tprops)
    print('\n\n')

    r = graphic.Shape('rectangle')
    rprops = {
        'strokeWidth': '2',
        'strokeColor': '0000',
        'fillColor': 'FFFFFFFFFaasdfasdfasdfFF',
    }
    r.validate_properties(rprops)
    print('\n\n', 'props now:', rprops)
    print('\n\n')
    '''

    # t.set_properties({'font-family': 'Wingdings', 'bold': 'qwerty', 'paddingTop': '3', })
    # print('\n\n', dump(t), '\n\n')

