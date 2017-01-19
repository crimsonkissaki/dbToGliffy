"""

"""

# Standard Library
import json
from pprint import PrettyPrinter
# Third Party
# Local
from . import shapes


# this is going to be ugly as sin as i figure out the best way to set it up
class Gliffy(object):
    """
    The main Gliffy adapter object.
    """

    # formatting options
    font = {
        'default': {
            'size': '12px',
            'font': 'Courier',
            'color': '#000000',
            'align': 'center'
        },
        'table_name': {
            'size': '14px',
        },
        'column_name': {
            'align': 'left'
        },
        'data_type': {
            'color': '#ff0000'
        }
    }

    def generate_gliffy_json(self):
        """
        Returns a JSON string for use in Gliffy

        :return:
        :rtype: str
        """
        stage = self.create_stage()
        return json.dumps(stage)

    def create_stage(self):
        return shapes.stage.copy()

    def group(self):
        g = shapes.Group()
        return g

    def text(self):
        t = shapes.Text()
        return t

    def line(self):
        l = shapes.Line()
        return l

    def rectangle(self):
        r = shapes.Rectangle()
        return r

    def create_group(self):
        return shapes.group.copy()

    def create_rectangle(self):
        return shapes.rectangle.copy()

    def create_text(self):
        return shapes.text.copy()

    def create_line(self):
        return shapes.line.copy()
