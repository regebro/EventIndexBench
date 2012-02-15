from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class UnindexView(BrowserView):
    """
    Unindex benchmark view
    """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def reindex_all(self):
        event_folder = self.portal.events
        objects = event_folder.objectValues('ATEvent')
       
        for ob in objects:
            self.portal_catalog.unindexObject(ob)
            
        return str(len(objects))
        