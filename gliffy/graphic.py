"""
Gliffy 'graphics' are the basic shapes, text, lines, etc.
"""

# Standard Library
import json
from collections import OrderedDict
# Third Party
# Local
from .base import GliffyObject
from utils import util


class Graphic(GliffyObject):
    """
    Base class for the Entity.graphic value. Graphics are used to display shapes, images, text, lines, etc.
    """

    __slots__ = ('type_def', 'graphic_type', 'properties')

    # tid value used in the graphic type def
    tids = {
        'circle': 'com.gliffy.stencil.ellipse.basic_v1',
        'square': 'com.gliffy.stencil.rectangle.basic_v1',
        'text': None,
        'line': False,
        # {} will be replaced by the graphic_type
        'default': 'com.gliffy.stencil.{}.basic_v1',
    }

    # uid value used in the entity type def
    uids = {
        'text': None,
        # {} will be replaced by the graphic_type
        'default': 'com.gliffy.shape.basic.basic_v1.default.{}',
    }

    def __init__(self):
        # type: () -> Graphic
        """
        :return: A Graphic object for use as an Entity.graphic value
        :rtype: Graphic
        """
        # these MUST be overridden in child classes
        self.graphic_type = 'UNDEFINED'
        self.type_def = {
            'type': 'UNDEFINED',
            'UNDEFINED': {}
        }
        # the modifiable Graphic properties - will be defined in child classes
        self.properties = {}

    @property
    def graphic_tid(self):
        # type: () -> Any
        """
        :return: A tid string; None if it's null; False if there is no 'tid' property.
        :rtype: :py:class:`Any`
        """
        graphic_type = self.graphic_type.lower()

        return self.tids.get(graphic_type, self.tids['default'].format(graphic_type))

    @property
    def entity_uid(self):
        # type: () -> Any
        """
        :return: A uid string; None if it's null.
        :rtype: Any
        """
        graphic_type = self.graphic_type.lower()

        return self.uids.get(graphic_type, self.uids['default'].format(graphic_type))

    def get_type_def(self):
        # type: () -> dict
        return self.type_def

    def to_json(self):
        # type: () -> str
        return json.dumps(self.get_type_def())


class Shape(Graphic):

    __slots__ = ('graphic_type', 'type_def', 'properties')

    def __init__(self, graphic_type, graphic_props={}):
        # type: (str, dict) -> Shape
        """
        Creates a new 'Shape' Graphic object for use in an Entity.

        :param str graphic_type: Type of Graphic to make.
        :param dict graphic_props: Properties to apply to the Graphic\n
                                   NOTE: These are properties defined by Gliffy and are camelCased!
        :keyword strokeWidth: (:py:class:`int`) Width of the shape's border
        :keyword strokeColor: (:py:class:`str`) Hex code for the shape's border color
        :keyword fillColor:   (:py:class:`str`) Hex code for the shape's fill color
        :rtype: Shape
        """
        super().__init__()
        self.graphic_type = graphic_type
        self.type_def = OrderedDict([
            ('type', 'Shape'),
            ('Shape', OrderedDict([
                ('tid', None),
                ('strokeWidth', 0),
                ('strokeColor', '#000000'),
                ('fillColor', '#FFFFFF'),
                ('gradient', False),
                ('dropShadow', False),
                ('state', 0),
                ('shadowX', 0),
                ('shadowY', 0),
                ('opacity', 1)
            ]))
        ])
        self.properties = {
            'strokeWidth': 2,
            'strokeColor': '#000000',
            'fillColor': '#FFFFFF',
        }
        self.set_properties(graphic_props)
        self.type_def['Shape']['tid'] = self.graphic_tid

    def set_properties(self, props):
        # type: (dict) -> Shape
        util.join_dicts(self.type_def['Shape'], self.properties, props)

        return self


class Text(Graphic):

    __slots__ = ('graphic_type', 'type_def', 'properties')

    def __init__(self, properties={}):
        # type: (dict) -> Text
        """
        Creates a 'Text' Graphic for use in an Entity

        :param dict properties: Properties to apply to the text.\n
                                NOTE: These are mostly actual CSS properties, so use -
        :keyword text:  (:py:class:`str`) Text to display
        :keyword css:   (:py:class:`dict`) CSS settings to apply to the text.\n
                        Valid properties are:\n
                        (:py:class:`str`):
                            ``text-align``  (left, middle, right)\n
                            ``font-size``   (9-14px, 18px, 24px, 36px, 48px)\n
                            ``font-family`` (Arial, Helvetica, Courier, Times, Verdana)\n
                            ``color``       (#xxxxxx)\n
                        (:py:class:`bool`):
                            ``bold``, ``italic``, ``underline``
        :rtype: Text
        """
        super().__init__()
        self.graphic_type = 'Text'
        self.type_def = OrderedDict([
            ('type', 'Text'),
            ('Text', OrderedDict([
                ('tid', None),
                ('valign', 'middle'),
                ('overflow', 'none'),
                ('vposition', 'none'),
                ('hposition', 'none'),
                ('html', '<p><span></span></p>'),
                ('paddingLeft', 2),
                ('paddingRight', 2),
                ('paddingBottom', 2),
                ('paddingTop', 2)
            ]))
        ])
        # customizable Text settings
        self.properties = {
            # the text to show
            'text': '',
            'css': {
                'text-align': 'center',
                'font-size': '12px',
                'font-family': 'Courier',
                'color': '#000000',
                'bold': False,
                'italic': False,
                'underline': False,
            },
        }
        self.set_properties(properties)

    def _set_html(self):
        txt = self.properties['text']
        css = self.properties['css']

        p_css = 'text-align: {};'.format(css['text-align'])
        css_props = ['font-size: {};', 'font-family: {};', 'white-space: pre-wrap;',
                     'text-decoration: {};', 'line-height: {};', 'color: {};']
        if css['bold']:
            css_props.append('font-weight: bold;')
        if css['italic']:
            css_props.append('font-style: italic;')
        text_dec = 'underline' if css['underline'] else 'none'
        span_css = ' '.join(css_props).format(css['font-size'], css['font-family'], text_dec,
                                              css['font-size'], css['color'])

        self.type_def['Text']['html'] = '<p style=\'{}\'><span style=\'{}\'>{}</span></p>'.format(p_css, span_css, txt)

    def set_properties(self, props):
        # type: (dict) -> Text
        util.join_dicts(self.properties, props)
        self._set_html()

        return self


# this class requires constraints be added
class Line(Graphic):

    __slots__ = ('graphic_type', 'type_def', 'properties')

    def __init__(self, properties={}):
        # type: (dict) -> Line
        """
        Creates a new 'Line' Graphic object for use in an Entity.

        :param dict properties: Properties to apply to the Graphic
        :keyword strokeWidth: (:py:class:`int`) Width of the line's border
        :keyword strokeColor: (:py:class:`str`) Hex code for the line's border color
        :rtype: Line
        """
        super().__init__()
        self.graphic_type = 'Line'
        self.type_def = {
            'type': 'Line',
            'Line': {
                'strokeWidth': 2,
                'strokeColor': '#000000',
                'fillColor': 'none',
                'dashStyle': None,
                'startArrow': 0,
                'endArrow': 1,
                'startArrowRotation': 'auto',
                'endArrowRotation': 'auto',
                'ortho': True,
                'interpolationType': 'linear',
                'cornerRadius': 10,
                'controlPath': [[9.740259795473818, 30.666666666666664], [9.740259795473818, 5.666666666666664],
                                [-14.906926462140476, 5.666666666666664], [-14.906926462140476, -19.333333333333336]],
                'lockSegments': {}
            }
        }
        self.properties = {
            'strokeWidth': 2,
            'strokeColor': '#000000',
        }
        self.set_properties(properties)

    def set_properties(self, props):
        # type: (dict) -> Line
        util.join_dicts(self.type_def['Line'], self.properties, props)

        return self
