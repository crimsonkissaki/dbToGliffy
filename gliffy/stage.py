"""
This is the 'stage' for Gliffy; the primary container for all objects.
"""

# Standard Library
import json
from collections import OrderedDict
# Third Party
# Local
from .base import GliffyObject


class Stage(GliffyObject):

    __slots__ = ('node_index', 'order', 'children', 'type_def')

    # json object definition
    def __init__(self):
        # iterator to keep elements numbered
        self.node_index = 0
        # z-index of elements
        self.order = 0
        self.children = []
        self.type_def = OrderedDict([
            ('contentType', 'application/gliffy+json'),
            ('version', '1.1'),
            ('metadata', OrderedDict([
                ('title', 'GliffyDB'),
                ('revision', 0),
                ('exportBorder', 'false')
            ])),
            ('embeddedResources', OrderedDict([
                ('index', 0),
                ('resources', [])
            ])),
            ('stage', OrderedDict([
                # entities go in objects
                ('objects', []),
                ('background', '#FFFFFF'),
                ('width', 0),  # TODO, this will need to be changed later
                ('height', 0),  # TODO, this will need to be changed later
                ('maxWidth', 5000),
                ('maxHeight', 5000),
                ('nodeIndex', 0),
                ('autoFit', True),
                ('exportBorder', False),
                ('gridOn', True),
                ('snapToGrid', True),
                ('drawingGuidesOn', True),
                ('pageBreaksOn', False),
                ('printGridOn', False),
                ('printPaper', 'LETTER'),
                ('printShrinkToFit', False),
                ('printPortrait', True),
                ('shapeStyles', {}),
                ('lineStyles', OrderedDict([
                    ('global', OrderedDict([
                        ('orthoMode', 1),
                        ('startArrow', 0),
                        ('endArrow', 1),
                        ('stroke', '#000000'),
                        ('dashStyle', None)
                    ]))
                ])),
                ('textStyles', {}),
                ('themeData', None),
            ]))
        ])

    def add(self, child):
        # type: (Entity) -> Stage
        self.children.append(child)
        self.reorder_children()
        self.update_coordinates()
        self.update_sizes()

        return self

    def reorder_children(self):
        pass

    def update_coordinates(self):
        pass

    def update_sizes(self):
        pass

    def get_type_def(self):
        # type: () -> dict
        # reset objects so we don't add copies
        self.type_def['stage']['objects'] = []
        for c in self.children:
            self.type_def['stage']['objects'].append(c.get_type_def())

        return self.type_def

    def to_json(self):
        # type: () -> str
        return json.dumps(self.get_type_def())
