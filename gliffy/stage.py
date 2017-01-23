"""
This is the 'stage' for Gliffy; the primary container for all objects.
"""

# Standard Library
import json
# Third Party
# Local


class Stage(object):
    # formatting options
    opts = {
        'title': 'GliffyDB'
    }

    # json object definition
    type_def = {
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
            'objects': [
                # the 'cells' go in here
            ],
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

    def __init__(self, **kwargs):
        self.opts['title'] = kwargs.get('title', 'GliffyDB')

    def add(self, child):
        self.type_def.stage.objects.append(child)

        return self



class placeholder():
    def __str__(self):
        self.typeDef['metadata']['title'] = self.title
        self.typeDef['stage']['width'] = self.width
        self.typeDef['stage']['height'] = self.height

        return json.dumps(self.typeDef)

    def add(self, obj):
        # type: (obj) -> Stage
        """
        Adds a Gliffy object to the stage

        :param obj obj: The object to add to the stage
        :return: Stage instance
        :rtype: Stage
        """
        if isinstance(obj, GliffyEntity):
            self.typeDef['stage']['objects'].append(obj)
        else:
            raise Exception('Unable to add invalid object type "{}" to Stage'.format(type(obj)))

        return self
