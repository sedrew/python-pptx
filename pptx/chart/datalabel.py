# encoding: utf-8

"""
Data label-related objects.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..text.text import Font
from ..util import lazyproperty


class DataLabels(object):
    """
    Collection of data labels associated with a plot, and perhaps with
    a series or data point, although the latter two are not yet implemented.
    """
    def __init__(self, dLbls):
        super(DataLabels, self).__init__()
        self._element = dLbls

    @lazyproperty
    def font(self):
        """
        The |Font| object that provides access to the text properties for
        these data labels, such as bold, italic, etc.
        """
        defRPr = self._element.defRPr
        font = Font(defRPr)
        return font

    @property
    def number_format(self):
        """
        Read/write string specifying the format for the numbers on this set
        of data labels. Returns 'General' if no number format has been set.
        Note that this format string has no effect on rendered data labels
        when :meth:`number_format_is_linked` is |True|. Assigning a format
        string to this property automatically sets
        :meth:`number_format_is_linked` to |False|.
        """
        numFmt = self._element.numFmt
        if numFmt is None:
            return 'General'
        return numFmt.formatCode

    @number_format.setter
    def number_format(self, value):
        self._element.get_or_add_numFmt().formatCode = value
        self.number_format_is_linked = False

    @property
    def number_format_is_linked(self):
        """
        Read/write boolean specifying whether number formatting should be
        taken from the source spreadsheet rather than the value of
        :meth:`number_format`.
        """
        numFmt = self._element.numFmt
        if numFmt is None:
            return True
        souceLinked = numFmt.sourceLinked
        if souceLinked is None:
            return True
        return numFmt.sourceLinked

    @number_format_is_linked.setter
    def number_format_is_linked(self, value):
        numFmt = self._element.get_or_add_numFmt()
        numFmt.sourceLinked = value

    @property
    def position(self):
        """
        Read/write :ref:`XlDataLabelPosition` enumeration value specifying
        the position of the data labels with respect to their data point, or
        |None| if no position is specified. Assigning |None| causes
        PowerPoint to choose the default position, which varies by chart
        type.
        """
        dLblPos = self._element.dLblPos
        if dLblPos is None:
            return None
        return dLblPos.val

    @position.setter
    def position(self, value):
        if value is None:
            self._element._remove_dLblPos()
            return
        self._element.get_or_add_dLblPos().val = value
