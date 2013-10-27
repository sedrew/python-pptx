# encoding: utf-8

"""
Namespace related objects.
"""

from __future__ import absolute_import


#: Maps namespace prefix to namespace name for all known PowerPoint XML
#: namespaces.
nsmap = {
    'a':   ('http://schemas.openxmlformats.org/drawingml/2006/main'),
    'cp':  ('http://schemas.openxmlformats.org/package/2006/metadata/core-pro'
            'perties'),
    'ct':  ('http://schemas.openxmlformats.org/package/2006/content-types'),
    'dc':  ('http://purl.org/dc/elements/1.1/'),
    'dcmitype': ('http://purl.org/dc/dcmitype/'),
    'dcterms':  ('http://purl.org/dc/terms/'),
    'ep':  ('http://schemas.openxmlformats.org/officeDocument/2006/extended-p'
            'roperties'),
    'i':   ('http://schemas.openxmlformats.org/officeDocument/2006/relationsh'
            'ips/image'),
    'm':   ('http://schemas.openxmlformats.org/officeDocument/2006/math'),
    'mo':  ('http://schemas.microsoft.com/office/mac/office/2008/main'),
    'mv':  ('urn:schemas-microsoft-com:mac:vml'),
    'o':   ('urn:schemas-microsoft-com:office:office'),
    'p':   ('http://schemas.openxmlformats.org/presentationml/2006/main'),
    'pd':  ('http://schemas.openxmlformats.org/drawingml/2006/presentationDra'
            'wing'),
    'pic': ('http://schemas.openxmlformats.org/drawingml/2006/picture'),
    'pr':  ('http://schemas.openxmlformats.org/package/2006/relationships'),
    'r':   ('http://schemas.openxmlformats.org/officeDocument/2006/relationsh'
            'ips'),
    'sl':  ('http://schemas.openxmlformats.org/officeDocument/2006/relationsh'
            'ips/slideLayout'),
    'v':   ('urn:schemas-microsoft-com:vml'),
    've':  ('http://schemas.openxmlformats.org/markup-compatibility/2006'),
    'w':   ('http://schemas.openxmlformats.org/wordprocessingml/2006/main'),
    'w10': ('urn:schemas-microsoft-com:office:word'),
    'wne': ('http://schemas.microsoft.com/office/word/2006/wordml'),
    'wp':  ('http://schemas.openxmlformats.org/drawingml/2006/wordprocessingD'
            'rawing'),
    'xsi': ('http://www.w3.org/2001/XMLSchema-instance')
}


def nsdecls(*prefixes):
    return ' '.join(['xmlns:%s="%s"' % (pfx, nsmap[pfx]) for pfx in prefixes])
