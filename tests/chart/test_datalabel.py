# encoding: utf-8

"""
Unit test suite for the pptx.chart.datalabel module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from pptx.chart.datalabel import DataLabels
from pptx.enum.chart import XL_LABEL_POSITION
from pptx.text.text import Font

from ..unitutil.cxml import element, xml
from ..unitutil.mock import class_mock, instance_mock


class DescribeDataLabels(object):

    def it_provides_access_to_its_font(self, font_fixture):
        data_labels, Font_, defRPr, font_ = font_fixture
        font = data_labels.font
        Font_.assert_called_once_with(defRPr)
        assert font is font_

    def it_adds_a_txPr_to_help_font(self, txPr_fixture):
        data_labels, expected_xml = txPr_fixture
        data_labels.font
        assert data_labels._element.xml == expected_xml

    def it_knows_its_number_format(self, number_format_get_fixture):
        data_labels, expected_value = number_format_get_fixture
        assert data_labels.number_format == expected_value

    def it_can_change_its_number_format(self, number_format_set_fixture):
        data_labels, new_value, expected_xml = number_format_set_fixture
        data_labels.number_format = new_value
        assert data_labels._element.xml == expected_xml

    def it_knows_whether_its_number_format_is_linked(
            self, number_format_is_linked_get_fixture):
        data_labels, expected_value = number_format_is_linked_get_fixture
        assert data_labels.number_format_is_linked is expected_value

    def it_can_change_whether_its_number_format_is_linked(
            self, number_format_is_linked_set_fixture):
        data_labels, new_value, expected_xml = (
            number_format_is_linked_set_fixture
        )
        data_labels.number_format_is_linked = new_value
        assert data_labels._element.xml == expected_xml

    def it_knows_its_position(self, position_get_fixture):
        data_labels, expected_value = position_get_fixture
        assert data_labels.position == expected_value

    def it_can_change_its_position(self, position_set_fixture):
        data_labels, new_value, expected_xml = position_set_fixture
        data_labels.position = new_value
        assert data_labels._element.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def font_fixture(self, Font_, font_):
        dLbls = element('c:dLbls/c:txPr/a:p/a:pPr/a:defRPr')
        defRPr = dLbls.xpath('.//a:defRPr')[0]
        data_labels = DataLabels(dLbls)
        return data_labels, Font_, defRPr, font_

    @pytest.fixture(params=[
        ('c:dLbls',                             'General'),
        ('c:dLbls/c:numFmt{formatCode=foobar}', 'foobar'),
    ])
    def number_format_get_fixture(self, request):
        dLbls_cxml, expected_value = request.param
        data_labels = DataLabels(element(dLbls_cxml))
        return data_labels, expected_value

    @pytest.fixture(params=[
        ('c:dLbls', 'General',
         'c:dLbls/c:numFmt{formatCode=General,sourceLinked=0}'),
        ('c:dLbls/c:numFmt{formatCode=General}', '00.00',
         'c:dLbls/c:numFmt{formatCode=00.00,sourceLinked=0}'),
    ])
    def number_format_set_fixture(self, request):
        dLbls_cxml, new_value, expected_dLbls_cxml = request.param
        data_labels = DataLabels(element(dLbls_cxml))
        expected_xml = xml(expected_dLbls_cxml)
        return data_labels, new_value, expected_xml

    @pytest.fixture(params=[
        ('c:dLbls',                          True),
        ('c:dLbls/c:numFmt',                 True),
        ('c:dLbls/c:numFmt{sourceLinked=0}', False),
        ('c:dLbls/c:numFmt{sourceLinked=1}', True),
    ])
    def number_format_is_linked_get_fixture(self, request):
        dLbls_cxml, expected_value = request.param
        data_labels = DataLabels(element(dLbls_cxml))
        return data_labels, expected_value

    @pytest.fixture(params=[
        ('c:dLbls', True,  'c:dLbls/c:numFmt{sourceLinked=1}'),
        ('c:dLbls', False, 'c:dLbls/c:numFmt{sourceLinked=0}'),
        ('c:dLbls', None,  'c:dLbls/c:numFmt'),
        ('c:dLbls/c:numFmt', True, 'c:dLbls/c:numFmt{sourceLinked=1}'),
        ('c:dLbls/c:numFmt{sourceLinked=1}', False,
         'c:dLbls/c:numFmt{sourceLinked=0}'),
    ])
    def number_format_is_linked_set_fixture(self, request):
        dLbls_cxml, new_value, expected_dLbls_cxml = request.param
        data_labels = DataLabels(element(dLbls_cxml))
        expected_xml = xml(expected_dLbls_cxml)
        return data_labels, new_value, expected_xml

    @pytest.fixture(params=[
        ('c:dLbls',                       None),
        ('c:dLbls/c:dLblPos{val=inBase}', XL_LABEL_POSITION.INSIDE_BASE),
    ])
    def position_get_fixture(self, request):
        dLbls_cxml, expected_value = request.param
        data_labels = DataLabels(element(dLbls_cxml))
        return data_labels, expected_value

    @pytest.fixture(params=[
        ('c:dLbls',                       XL_LABEL_POSITION.INSIDE_BASE,
         'c:dLbls/c:dLblPos{val=inBase}'),
        ('c:dLbls/c:dLblPos{val=inBase}', XL_LABEL_POSITION.OUTSIDE_END,
         'c:dLbls/c:dLblPos{val=outEnd}'),
        ('c:dLbls/c:dLblPos{val=inBase}', None, 'c:dLbls'),
        ('c:dLbls',                       None, 'c:dLbls'),
    ])
    def position_set_fixture(self, request):
        dLbls_cxml, new_value, expected_dLbls_cxml = request.param
        data_labels = DataLabels(element(dLbls_cxml))
        expected_xml = xml(expected_dLbls_cxml)
        return data_labels, new_value, expected_xml

    @pytest.fixture(params=[
        ('c:dLbls{a:b=c}',
         'c:dLbls{a:b=c}/c:txPr/(a:bodyPr,a:lstStyle,a:p/a:pPr/a:defRPr)'),
        ('c:dLbls{a:b=c}/c:txPr/(a:bodyPr,a:p)',
         'c:dLbls{a:b=c}/c:txPr/(a:bodyPr,a:p/a:pPr/a:defRPr)'),
        ('c:dLbls{a:b=c}/c:txPr/(a:bodyPr,a:p/a:pPr)',
         'c:dLbls{a:b=c}/c:txPr/(a:bodyPr,a:p/a:pPr/a:defRPr)'),
    ])
    def txPr_fixture(self, request):
        dLbls_cxml, expected_cxml = request.param
        data_labels = DataLabels(element(dLbls_cxml))
        expected_xml = xml(expected_cxml)
        return data_labels, expected_xml

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Font_(self, request, font_):
        return class_mock(
            request, 'pptx.chart.datalabel.Font', return_value=font_
        )

    @pytest.fixture
    def font_(self, request):
        return instance_mock(request, Font)
