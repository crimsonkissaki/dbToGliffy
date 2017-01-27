"""
Gliffy 'graphics' are the basic shapes, text, lines, etc.
"""

# Standard Library
import json
from collections import OrderedDict
# Third Party
# Local
from .base import GliffyObject
from utils import util, validate


class Graphic(GliffyObject):
    """
    Base class for the Entity.graphic value. Graphics are used to display shapes, images, text, lines, etc.
    """

    __slots__ = ('type_def', 'graphic_type', 'properties')

    defaults = {}
    bad_val_err = '\n\n----- @@@ ERROR: Invalid `({}) {}` value `{}` -----\n\n'

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

    def check_values(self, dic, keys, data_type, convert=False):
        # type: (dict, list, Any, bool) -> None
        """
        Simplified value checker.

        :param dict dic: The dict to check values in
        :param list keys: The keys to check in the dict
        :param Any data_type: The data type to check. Mostly built-in types (int, str, bool, etc)
        :param bool convert: Flag to (en|dis)able attempted conversions
        :rtype: None
        """
        if not dic:
            return
        hex_check = False
        if data_type == 'hex':
            hex_check = True
            data_type = str
        for k in keys:
            valid = validate.in_dict_as_type(dic, k, data_type, convert)
            if valid is False:
                print(self.bad_val_err.format(data_type.__name__, k, keys[k]))
                dic[k] = self.defaults[k]
            elif valid is not None:
                if hex_check and not dic[k].startswith('#'):
                    dic[k] = '#'+dic[k][0:6]

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

    # default property values - these are Class properties & can be set without having a Shape instance
    defaults = {
        'strokeWidth': 2,
        'strokeColor': '#000000',
        'fillColor': '#FFFFFF',
    }

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
        self.properties = self.defaults.copy()
        self.set_properties(graphic_props)
        self.type_def['Shape']['tid'] = self.graphic_tid

    def validate_properties(self, props={}):
        # type: (dict) -> None
        """
        Validates user-supplied properties to be applied to the Shape Graphic.

        Invalid values will be replaced by the defaults.
        """
        if not props:
            return
        self.check_values(props, ['strokeWidth'], int, True)
        self.check_values(props, ['strokeColor', 'fillColor'], 'hex', True)

    def set_properties(self, props):
        # type: (dict) -> Shape
        util.join_dicts(self.type_def['Shape'], self.properties, props)

        return self


class Text(Graphic):
    """
    A Gliffy Graphic that is used to display text.

    You can override the default values without instantiating the object by
    manually setting ``graphic.Text.defaults`` before any are created.
    """

    __slots__ = ('graphic_type', 'type_def', 'properties')

    # valid property values
    valid = {
        'text-align': ('left', 'middle', 'right'),
        'font-family': ('Arial', 'Helvetica', 'Courier', 'Times', 'Verdana'),
        'font-size': ('9px', '10px', '11px', '12px', '13px', '14px', '18px', '24px', '36px', '48px'),
    }
    # default property values - these are Class properties & can be set without having a Text instance
    defaults = {
        'color': '#000000',
        'text-align': 'middle',
        'font-family': 'Courier',
        'font-size': '12px',
        'bold': False,
        'italic': False,
        'underline': False,
        'paddingVert': 2,
        'paddingHoriz': 2,
        'paddingLeft': 2,
        'paddingRight': 2,
        'paddingBottom': 2,
        'paddingTop': 2,
    }

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
                            ``text-align``  left, middle, right (Default middle)\n
                            ``font-size``   9-14px, 18px, 24px, 36px, 48px (Default 12px)\n
                            ``font-family`` Arial, Helvetica, Courier, Times, Verdana (Default Courier)\n
                            ``color``       #xxxxxx (Default #000000)\n
                        (:py:class:`bool`):
                            ``bold``, ``italic``, ``underline``
                        (:py:class:`int`):
                            ``paddingLeft``, ``paddingRight``, ``paddingBottom``, ``paddingTop``
                            ``paddingVert`` (sets ``paddingTop`` & ``paddingBottom``)
                            ``paddingHoriz`` (sets ``paddingLeft`` & ``paddingRight``)
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
                ('paddingLeft', 0),
                ('paddingRight', 0),
                ('paddingBottom', 0),
                ('paddingTop', 0)
            ]))
        ])
        # customizable Text settings
        self.properties = {
            # the text to show
            'text': '',
            'css': self.defaults.copy(),
        }
        self.set_properties(properties)

    def set_properties(self, props={}):
        # type: (dict) -> Text
        """
        Updates the Text Graphic's properties with supplied values.

        Invalid property values will fail silently and be replaced with the default values

        :param dict props: Properties to assign to the Text
        :return: Text Entity for method chaining
        :rtype: Text
        """
        if not props:
            return self

        self.validate_properties(props)
        css = self.properties['css']
        if css['paddingVert']:
            css['paddingTop'] = css['paddingBottom'] = css['paddingVert']
        if css['paddingHoriz']:
            css['paddingLeft'] = css['paddingRight'] = css['paddingHoriz']

        util.join_dicts(self.properties, props)
        self._set_html()

        return self

    def validate_properties(self, props={}):
        # type: (dict) -> None
        """
        Validates user-supplied properties to be applied to the Text Graphic.

        Invalid values will be replaced by the defaults.
        """
        if not props:
            return
        if 'css' in props:
            props = props['css']

        # f = {k: 'bork' for k in c.keys() & d.keys() if c[k] != d[k]}
        for v in self.valid.keys() & props.keys():  # intersection
            if props[v] not in self.valid[v]:
                print(self.bad_val_err.format('css', v, props[v]))
                props[v] = self.defaults[v]
        self.check_values(props, ['color'], 'hex', True)
        self.check_values(props, ['bold', 'italic', 'underline'], bool, True)
        self.check_values(props, ['padding' + k for k in ['Vert', 'Horiz', 'Top', 'Bottom', 'Left', 'Right']], int, True)

    def _set_html(self):
        # type: () -> None
        """
        Sets the Text Graphic's ``html`` property based on supplied/default CSS settings
        """
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


# this class requires constraints be added
class Line(Graphic):

    __slots__ = ('graphic_type', 'type_def', 'properties')

    defaults = {
        'strokeWidth': 2,
        'strokeColor': '#000000',
    }

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
                'strokeWidth': 0,
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

    def validate_properties(self, props={}):
        # type: (dict) -> None
        """
        Validates user-supplied properties to be applied to the Line Graphic.

        Invalid values will be replaced by the defaults.
        """
        if not props:
            return
        self.check_values(props, ['strokeWidth'], int, True)
        self.check_values(props, ['strokeColor'], 'hex', True)

    def set_properties(self, props):
        # type: (dict) -> Line
        self.validate_properties(props)
        util.join_dicts(self.type_def['Line'], self.properties, props)

        return self
