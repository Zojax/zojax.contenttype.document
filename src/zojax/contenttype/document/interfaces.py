##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" document interfaces

$Id$
"""
from zope import schema, interface
from zojax.richtext.field import RichText
from zojax.contenttypes.interfaces import _


class IDocument(interface.Interface):

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'document title.'),
        default = u'',
        missing_value = u'',
        required = True)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'A short summary of the document.'),
        default = u'',
        missing_value = u'',
        required = False)

    text = RichText(
        title = _(u'Body'),
        description = _(u'Document body text.'),
        required = True)


class IDocumentType(interface.Interface):
    """ document content type """
