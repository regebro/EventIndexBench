from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class ReindexView(BrowserView):
    """
    Reindex benchmark view
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
        indexes = self.request['indexes'].split(',')
        
        event_folder = self.portal.events
        objects = event_folder.objectValues('ATEvent')
       
        for ob in objects:
            self.portal_catalog.reindexObject(ob, indexes)
            
        return str(len(objects))
        