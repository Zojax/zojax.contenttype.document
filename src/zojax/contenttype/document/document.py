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
""" document implementation

$Id$
"""
from zope import interface, component
from zope.size import byteDisplay
from zope.size.interfaces import ISized
from zojax.content.type.item import PersistentItem
from zojax.content.type.interfaces import IItemPublishing
from zojax.content.type.searchable import ContentSearchableText
from zojax.richtext.field import RichTextProperty
from zojax.content.revision.revisions import Revisions, IRevisions

from interfaces import IDocument


class Document(PersistentItem, Revisions):
    interface.implements(IDocument, IItemPublishing, IRevisions)

    __contentschema__ = IDocument
    __contentfields__ = {'text': RichTextProperty(IDocument['text'])}


class Sized(object):
    component.adapts(IDocument)
    interface.implements(ISized)

    def __init__(self, context):
        self.context = context

        self.size = len(context.title) + \
                    len(context.description) + \
                    len(context.text)

    def sizeForSorting(self):
        return "byte", self.size

    def sizeForDisplay(self):
        return byteDisplay(self.size)


class DocumentSearchableText(ContentSearchableText):
    component.adapts(IDocument)

    def getSearchableText(self):
        text = super(DocumentSearchableText, self).getSearchableText()
        try:
            return text + u' ' + self.content.text.text
        except AttributeError:
            return text
