# encoding: utf-8

"""Test data for unit tests"""

from pptx.oxml import oxml_fromstring
from pptx.oxml.ns import nsdecls
from pptx.shapes.shapetree import Picture, Shape, ShapeCollection
from pptx.shapes.table import _Cell
from pptx.text import _Paragraph


class CT_CorePropertiesBuilder(object):
    """
    Test data builder for CT_CoreProperties (cp:coreProperties) XML element
    """
    properties = (
        ('author',           'dc:creator'),
        ('category',         'cp:category'),
        ('comments',         'dc:description'),
        ('content_status',   'cp:contentStatus'),
        ('created',          'dcterms:created'),
        ('identifier',       'dc:identifier'),
        ('keywords',         'cp:keywords'),
        ('language',         'dc:language'),
        ('last_modified_by', 'cp:lastModifiedBy'),
        ('last_printed',     'cp:lastPrinted'),
        ('modified',         'dcterms:modified'),
        ('revision',         'cp:revision'),
        ('subject',          'dc:subject'),
        ('title',            'dc:title'),
        ('version',          'cp:version'),
    )

    def __init__(self):
        """Establish instance variables with default values"""
        for propname, tag in self.properties:
            setattr(self, '_%s' % propname, None)

    @property
    def _ns_prefixes(self):
        ns_prefixes = ['cp', 'dc', 'dcterms']
        for propname, tag in self.properties:
            value = getattr(self, '_%s' % propname)
            if value is None:
                continue
            ns_prefix = tag.split(':')[0]
            if ns_prefix not in ns_prefixes:
                ns_prefixes.append(ns_prefix)
            if ns_prefix == 'dcterms' and 'xsi' not in ns_prefixes:
                ns_prefixes.append('xsi')
        return tuple(ns_prefixes)

    @property
    def props_xml(self):
        props_xml = ''
        for propname, tag in self.properties:
            value = getattr(self, '_%s' % propname)
            if value is None:
                continue
            if value == '':
                xml = '  <%s/>\n' % tag
            else:
                if tag.startswith('dcterms:'):
                    xml = ('  <%s xsi:type="dcterms:W3CDTF">%s</%s>\n' %
                           (tag, value, tag))
                else:
                    xml = '  <%s>%s</%s>\n' % (tag, value, tag)
            props_xml += xml
        return props_xml

    @property
    def coreProperties(self):
        if self.props_xml:
            coreProperties = (
                '<cp:coreProperties %s>\n%s</cp:coreProperties>\n' %
                (nsdecls(*self._ns_prefixes), self.props_xml)
            )
        else:
            coreProperties = (
                '<cp:coreProperties %s/>\n' % nsdecls('cp', 'dc', 'dcterms')
            )
        return coreProperties

    @property
    def element(self):
        """Return element based on XML generated by builder"""
        return oxml_fromstring(self.xml)

    def with_child(self, name, value):
        """add property element for *name* set to *value*"""
        setattr(self, '_%s' % name, value)
        return self

    def with_date_prop(self, name, value):
        """add date property element for *name* set to *value*"""
        setattr(self, '_%s' % name, value)
        return self

    def with_revision(self, value):
        """add revision element set to *value*"""
        self._revision = value
        return self

    @property
    def xml(self):
        """
        Return XML string based on settings accumulated via method calls
        """
        return self.coreProperties


class CT_PresetGeometry2DBuilder(object):
    """
    Test data builder for CT_PresetGeometry2D (prstGeom) XML element
    """
    def __init__(self, prst='rect'):
        """Establish instance variables with default values"""
        self._prst = prst
        self._avLst = False
        self._guides = []

    @property
    def with_avLst(self):
        """contains an <a:avLst> element, even if it's empty"""
        self._avLst = True
        return self

    def with_gd(self, val=25000, name='adj'):
        """add <a:gd> element"""
        self._guides.append((name, val))
        return self

    @property
    def avLst(self):
        if self.gd:
            avLst = '  <a:avLst>\n%s  </a:avLst>\n' % self.gd
        elif self._avLst:
            avLst = '  <a:avLst/>\n'
        else:
            avLst = ''
        return avLst

    @property
    def gd(self):
        if self._guides:
            tmpl = '    <a:gd name="%s" fmla="val %d"/>\n'
            gd = ''.join([tmpl % guide for guide in self._guides])
        else:
            gd = ''
        return gd

    @property
    def prstGeom(self):
        if self.avLst:
            prstGeom = ('<a:prstGeom %s prst="%s">\n%s</a:prstGeom>\n' %
                        (nsdecls('a'), self._prst, self.avLst))
        else:
            prstGeom = ('<a:prstGeom %s prst="%s"/>\n' %
                        (nsdecls('a'), self._prst))
        return prstGeom

    def reset(self):
        """return guides and avLst to defaults"""
        self._avLst = False
        self._guides = []

    @property
    def xml(self):
        """
        Return XML string based on settings accumulated via method calls
        """
        return self.prstGeom

    @property
    def element(self):
        """Return element based on XML generated by builder"""
        return oxml_fromstring(self.xml)


class CT_TableBuilder(object):
    """Test data builder for CT_Table (tbl) XML element"""
    empty_tbl_tmpl = (
        '<a:tbl %s/>%s\n'
    )
    with_props_tmpl = (
        '<a:tbl %s>\n'
        '  <a:tblPr%s/>\n'
        '</a:tbl>\n'
    )

    def __init__(self):
        """Establish instance variables with default values"""
        self._tmpl = CT_TableBuilder.empty_tbl_tmpl
        self._properties = []

    @property
    def _tblPr_attrs_str(self):
        """String containing all attributes of tblPr element"""
        s = ''
        for prop in self._properties:
            s += ' %s="%s"' % prop
        return s

    @property
    def xml(self):
        """
        Return XML string based on settings accumulated via method calls
        """
        return self._tmpl % (nsdecls('a'), self._tblPr_attrs_str)

    @property
    def element(self):
        """Return element based on XML generated by builder"""
        return oxml_fromstring(self.xml)

    @property
    def with_tblPr(self):
        """include tblPr element even if it's empty"""
        self._tmpl = CT_TableBuilder.with_props_tmpl
        return self

    def with_prop(self, name, value):
        """add property named *name* with specified *value*"""
        self._tmpl = CT_TableBuilder.with_props_tmpl
        self._properties.append((name, value))
        return self


def a_coreProperties():
    """Syntactic sugar to construct a CT_CorePropertiesBuilder instance"""
    return CT_CorePropertiesBuilder()


def a_prstGeom(prst='rect'):
    """Syntactic sugar to construct a CT_PresetGeometry2DBuilder instance"""
    return CT_PresetGeometry2DBuilder(prst)


def a_tbl():
    """Syntactic sugar to construct a CT_TableBuilder"""
    return CT_TableBuilder()


class _TestShapeXml(object):
    """XML snippets of various shapes for use in unit tests"""
    @property
    def autoshape(self):
        """
        XML for an autoshape for unit testing purposes, a rounded rectangle in
        this case.
        """
        return (
            '<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/'
            '2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/'
            '2006/main"><p:nvSpPr><p:cNvPr id="3" name="Rounded Rectangle 2"/'
            '><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="76009'
            '6" y="562720"/><a:ext cx="2520824" cy="914400"/></a:xfrm><a:prst'
            'Geom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 30346"'
            '/></a:avLst></a:prstGeom></p:spPr><p:style><a:lnRef idx="1"><a:s'
            'chemeClr val="accent1"/></a:lnRef><a:fillRef idx="3"><a:schemeCl'
            'r val="accent1"/></a:fillRef><a:effectRef idx="2"><a:schemeClr v'
            'al="accent1"/></a:effectRef><a:fontRef idx="minor"><a:schemeClr '
            'val="lt1"/></a:fontRef></p:style><p:txBody><a:bodyPr rtlCol="0" '
            'anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"/><a:r><a:rPr l'
            'ang="en-US" dirty="0" smtClean="0"/><a:t>This is text inside a r'
            'ounded rectangle</a:t></a:r><a:endParaRPr lang="en-US" dirty="0"'
            '/></a:p></p:txBody></p:sp>'
        )

    @property
    def empty_spTree(self):
        return (
            '<p:spTree %s>\n'
            '  <p:nvGrpSpPr>\n'
            '    <p:cNvPr id="1" name=""/>\n'
            '    <p:cNvGrpSpPr/>\n'
            '    <p:nvPr/>\n'
            '  </p:nvGrpSpPr>\n'
            '  <p:grpSpPr/>\n'
            '</p:spTree>\n' % nsdecls('p', 'a')
        )

    @property
    def picture(self):
        """ XML for an pic shape, for unit testing purposes """
        return (
            '<p:pic %s>\n'
            '  <p:nvPicPr>\n'
            '    <p:cNvPr id="9" name="Picture 8" descr="image.png"/>\n'
            '    <p:cNvPicPr>\n'
            '      <a:picLocks noChangeAspect="1"/>\n'
            '    </p:cNvPicPr>\n'
            '    <p:nvPr/>\n'
            '  </p:nvPicPr>\n'
            '  <p:blipFill>\n'
            '    <a:blip r:embed="rId7"/>\n'
            '    <a:stretch>\n'
            '      <a:fillRect/>\n'
            '    </a:stretch>\n'
            '  </p:blipFill>\n'
            '  <p:spPr>\n'
            '    <a:xfrm>\n'
            '      <a:off x="111" y="222"/>\n'
            '      <a:ext cx="333" cy="444"/>\n'
            '    </a:xfrm>\n'
            '    <a:prstGeom prst="rect">\n'
            '      <a:avLst/>\n'
            '    </a:prstGeom>\n'
            '  </p:spPr>\n'
            '</p:pic>\n' % nsdecls('a', 'p', 'r')
        )

    @property
    def placeholder(self):
        """Generic placeholder XML, a date placeholder in this case"""
        return (
            '<p:sp xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/'
            'main" xmlns:p="http://schemas.openxmlformats.org/presentationml/'
            '2006/main">\n'
            '  <p:nvSpPr>\n'
            '    <p:cNvPr id="9" name="Date Placeholder 8"/>\n'
            '    <p:cNvSpPr>\n'
            '      <a:spLocks noGrp="1"/>\n'
            '    </p:cNvSpPr>\n'
            '    <p:nvPr>\n'
            '      <p:ph type="dt" sz="half" idx="10"/>\n'
            '    </p:nvPr>\n'
            '  </p:nvSpPr>\n'
            '  <p:spPr/>\n'
            '</p:sp>\n'
        )

    @property
    def rounded_rectangle(self):
        """XML for a rounded rectangle auto shape"""
        return self.autoshape

    @property
    def textbox(self):
        """Generic text box XML"""
        return (
            '<p:sp %s>\n'
            '  <p:nvSpPr>\n'
            '    <p:cNvPr id="9" name="TextBox 8"/>\n'
            '    <p:cNvSpPr txBox="1"/>\n'
            '    <p:nvPr/>\n'
            '  </p:nvSpPr>\n'
            '  <p:spPr>\n'
            '    <a:xfrm>\n'
            '      <a:off x="111" y="222"/>\n'
            '      <a:ext cx="333" cy="444"/>\n'
            '    </a:xfrm>\n'
            '    <a:prstGeom prst="rect">\n'
            '      <a:avLst/>\n'
            '    </a:prstGeom>\n'
            '    <a:noFill/>\n'
            '  </p:spPr>\n'
            '  <p:txBody>\n'
            '    <a:bodyPr wrap="none">\n'
            '      <a:spAutoFit/>\n'
            '    </a:bodyPr>\n'
            '    <a:lstStyle/>\n'
            '    <a:p/>\n'
            '  </p:txBody>\n'
            '</p:sp>' % nsdecls('a', 'p')
        )


test_shape_xml = _TestShapeXml()


class _TestTableXml(object):
    """XML snippets of table-related elements for use in unit tests"""
    @property
    def cell(self):
        """
        XML for empty default table cell
        """
        return (
            '<a:tc %s>\n'
            '  <a:txBody>\n'
            '    <a:bodyPr/>\n'
            '    <a:lstStyle/>\n'
            '    <a:p/>\n'
            '  </a:txBody>\n'
            '</a:tc>\n' % nsdecls('a')
        )

    @property
    def cell_with_margins(self):
        """
        XML for cell having top, left, right, and bottom margin settings
        """
        return (
            '<a:tc %s>\n'
            '  <a:txBody>\n'
            '    <a:bodyPr/>\n'
            '    <a:lstStyle/>\n'
            '    <a:p/>\n'
            '  </a:txBody>\n'
            '  <a:tcPr marT="12" marR="34" marB="56" marL="78"/>\n'
            '</a:tc>\n' % nsdecls('a')
        )

    @property
    def top_aligned_cell(self):
        """
        XML for empty top-aligned table cell
        """
        return (
            '<a:tc %s>\n'
            '  <a:txBody>\n'
            '    <a:bodyPr/>\n'
            '    <a:lstStyle/>\n'
            '    <a:p/>\n'
            '  </a:txBody>\n'
            '  <a:tcPr anchor="t"/>\n'
            '</a:tc>\n' % nsdecls('a')
        )


test_table_xml = _TestTableXml()


class _TestTextXml(object):
    """XML snippets of text-related elements for use in unit tests"""
    @property
    def centered_paragraph(self):
        """
        XML for centered paragraph
        """
        return (
            '<a:p %s>\n'
            '  <a:pPr algn="ctr"/>\n'
            '</a:p>\n' % nsdecls('a')
        )

    @property
    def paragraph(self):
        """
        XML for a default, empty paragraph
        """
        return '<a:p %s/>\n' % nsdecls('a')


test_text_xml = _TestTextXml()


class _TestShapeElements(object):
    """Shape elements for use in unit tests"""
    @property
    def autoshape(self):
        return oxml_fromstring(test_shape_xml.autoshape)

    @property
    def empty_spTree(self):
        return oxml_fromstring(test_shape_xml.empty_spTree)

    @property
    def picture(self):
        return oxml_fromstring(test_shape_xml.picture)

    @property
    def placeholder(self):
        return oxml_fromstring(test_shape_xml.placeholder)

    @property
    def rounded_rectangle(self):
        return oxml_fromstring(test_shape_xml.rounded_rectangle)

    @property
    def textbox(self):
        return oxml_fromstring(test_shape_xml.textbox)


test_shape_elements = _TestShapeElements()


class _TestTableElements(object):
    """Table-related elements for use in unit tests"""
    @property
    def cell(self):
        return oxml_fromstring(test_table_xml.cell)

    @property
    def cell_with_margins(self):
        return oxml_fromstring(test_table_xml.cell_with_margins)

    @property
    def isolated_tbl(self):
        return oxml_fromstring(test_table_xml.isolated_tbl)

    @property
    def isolated_tbl_with_true_props(self):
        return oxml_fromstring(test_table_xml.isolated_tbl_with_true_props)

    @property
    def top_aligned_cell(self):
        return oxml_fromstring(test_table_xml.top_aligned_cell)


test_table_elements = _TestTableElements()


class _TestTextElements(object):
    """Text elements for use in unit tests"""
    @property
    def centered_paragraph(self):
        return oxml_fromstring(test_text_xml.centered_paragraph)

    @property
    def paragraph(self):
        return oxml_fromstring(test_text_xml.paragraph)


test_text_elements = _TestTextElements()


class _TestShapes(object):
    """Shape instances for use in unit tests"""
    @property
    def autoshape(self):
        return Shape(test_shape_elements.autoshape)

    @property
    def empty_shape_collection(self):
        return ShapeCollection(test_shape_elements.empty_spTree)

    @property
    def picture(self):
        return Picture(test_shape_elements.picture)

    @property
    def placeholder(self):
        return Shape(test_shape_elements.placeholder)

    @property
    def rounded_rectangle(self):
        return Shape(test_shape_elements.rounded_rectangle)

    @property
    def textbox(self):
        return Shape(test_shape_elements.textbox)


test_shapes = _TestShapes()


class _TestTableObjects(object):
    """Table-related object instances for use in unit tests"""
    @property
    def cell(self):
        return _Cell(test_table_elements.cell)


test_table_objects = _TestTableObjects()


class _TestTextObjects(object):
    """Text object instances for use in unit tests"""
    @property
    def paragraph(self):
        return _Paragraph(test_text_elements.paragraph)


test_text_objects = _TestTextObjects()
