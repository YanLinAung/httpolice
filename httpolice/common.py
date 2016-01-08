# -*- coding: utf-8; -*-

from collections import namedtuple


class ReportNode(object):

    self_name = 'self'

    def __init__(self):
        self.complaints = None
        self.annotated = None

    def complain(self, notice_ident, **kwargs):
        if self.complaints is None:
            self.complaints = []
        context = dict({self.self_name: self}, **kwargs)
        complaint = (notice_ident, context)
        if complaint not in self.complaints:
            self.complaints.append(complaint)


class _Unparseable(object):

    __slots__ = ()

    def __repr__(self):
        return 'Unparseable'

Unparseable = _Unparseable()


def okay(x):
    return (x is not None) and (x is not Unparseable)


class Citation(namedtuple('Citation', ('title', 'url'))):

    __slots__ = ()
    __unicode__ = lambda self: self.title


def rfc(num, *section):
    title = u'RFC %d' % num
    url = u'http://tools.ietf.org/html/rfc%d' % num
    if section:
        section_text = u'.'.join(unicode(n) for n in section)
        if section_text[0].isalpha():
            title += u' appendix %s' % section_text
            url += u'#appendix-%s' % section_text
        else:
            title += u' § %s' % section_text
            url += u'#section-%s' % section_text
    return Citation(title, url)


class ProtocolString(unicode):

    __slots__ = ()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, unicode.__repr__(self))


class CaseInsensitive(ProtocolString):

    __slots__ = ()

    def __eq__(self, other):
        if isinstance(other, basestring):
            return self.lower() == other.lower()
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.lower())


class Parametrized(namedtuple('Parametrized', ('item', 'param'))):

    __slots__ = ()

    def __eq__(self, other):
        return (self.item == other) or super(Parametrized, self).__eq__(other)

    def __ne__(self, other):
        return (self.item != other) and super(Parametrized, self).__ne__(other)


class OriginForm(ProtocolString):

    __slots__ = ()


class AsteriskForm(ProtocolString):

    __slots__ = ()


class Known(object):

    def __init__(self, items):
        self._by_key = dict((self._key_for(item), item) for item in items)
        self._by_name = dict((self._name_for(item), item) for item in items)

    def __getattr__(self, name):
        if name in self._by_name:
            return self._key_for(self._by_name[name])
        else:
            raise AttributeError(name)

    def __getitem__(self, key):
        return self._by_key[key]

    def get_info(self, key):
        return self._by_key.get(key, {})

    def __iter__(self):
        return iter(self._by_key)

    def __contains__(self, key):
        return key in self._by_key

    @classmethod
    def _key_for(cls, item):
        return item['name']

    @classmethod
    def _name_for(cls, item):
        return item['name'].replace(u'-', u' ').replace(u' ', u'_').lower()
