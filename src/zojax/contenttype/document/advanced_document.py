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
from z3c.form.object import registerFactoryAdapter
from zojax.content.type.searchable import ContentSearchableText
from zope import interface, component
from zojax.content.type.item import PersistentItem
from zojax.content.type.interfaces import IItemPublishing
from zojax.richtext.field import RichTextProperty
from zojax.content.revision.revisions import Revisions, IRevisions
from zope.schema.fieldproperty import FieldProperty
from interfaces import IDocument, IAdvancedDocument, IDocumentTab
from document import Document
from zope.size import byteDisplay
from zope.size.interfaces import ISized
from rwproperty import setproperty, getproperty


class AdvancedDocument(Document):
    interface.implements(IAdvancedDocument, IItemPublishing, IRevisions)

    __contentschema__ = IAdvancedDocument
    __contentfields__ = {'text': RichTextProperty(IAdvancedDocument['text'])}


    @getproperty
    def tabs(self):
        return self.__dict__.get('tabs', [])

    @setproperty
    def tabs(self, value):
        old = self.tabs
        if value is not None:
            if len(value) > len(old):
                old.extend(value[len(old):])
            else:
                old = old[:len(value)]
        else:
            self.__data__['tabs'] = []
            return
        for k, v in enumerate(value):
            ov = old[k]
            if v.text:
                ov.text = v.text
            ov.position = v.position

        # NOTE: sort by position
        old = sorted(old, key=lambda x: x.position)
        self.__dict__['tabs'] = old

    @property
    def text(self):
        return ''.join([getattr(tab.text, 'cooked', '') for tab in self.tabs])


class DocumentTab(object):
    interface.implements(IDocumentTab)

    title = None
    text = RichTextProperty(IDocumentTab['text'])
    position = FieldProperty(IDocumentTab['position'])

registerFactoryAdapter(IDocumentTab, DocumentTab)


class Sized(object):
    component.adapts(IAdvancedDocument)
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
    component.adapts(IAdvancedDocument)

    def getSearchableText(self):
        text = super(DocumentSearchableText, self).getSearchableText()
        try:
            return text + u' ' + self.content.text.text
        except AttributeError:
            return text



