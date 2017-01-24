"""
This is the 'stage' for Gliffy; the primary container for all objects.
"""

# Standard Library
import json
# Third Party
# Local
from .base import GliffyObject


class Stage(GliffyObject):

    __slots__ = ('children', 'type_def')

    # json object definition
    def __init__(self):
        self.children = []
        self.type_def = {
            'contentType': 'application/gliffy+json',
            'version': '1.1',
            'metadata': {
                'title': 'GliffyDB',
                'revision': 0,
                'exportBorder': 'false'
            },
            'embeddedResources': {
                'index': 0,
                'resources': []
            },
            'stage': {
                # entities go in objects
                'objects': [],
                'background': '#FFFFFF',
                'width': 0,  # TODO: this will need to be changed later
                'height': 0,  # TODO: this will need to be changed later
                'maxWidth': 5000,
                'maxHeight': 5000,
                'nodeIndex': 0,
                'autoFit': True,
                'exportBorder': False,
                'gridOn': True,
                'snapToGrid': True,
                'drawingGuidesOn': True,
                'pageBreaksOn': False,
                'printGridOn': False,
                'printPaper': 'LETTER',
                'printShrinkToFit': False,
                'printPortrait': True,
                'shapeStyles': {},
                'lineStyles': {
                    'global': {
                        'orthoMode': 1,
                        'startArrow': 0,
                        'endArrow': 1,
                        'stroke': '#000000',
                        'dashStyle': None
                    }
                },
                'textStyles': {},
                'themeData': None
            }
        }

    def __str__(self):
        return self.to_json()

    def add_child(self, child):
        self.children.append(child)

        return self

    def to_json(self):
        # type: () -> str
        for c in self.children:
            self.type_def['stage']['objects'].append(c.get_type_def())

        return json.dumps(self.type_def)
