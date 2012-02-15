from datetime import datetime
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ZCatalog import ZCatalog

class QueryView(BrowserView):
    """
    Query benchmark view
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

    def query(self):
        query = {}
        if 'start' in self.request:
            query['start'] = {
                'query': datetime.strptime(self.request['start'], '%Y-%m-%d %H:%M'),
                'range': 'min',
            }
                
        if 'end' in self.request:
            query['end'] = {
                'query': datetime.strptime(self.request['end'], '%Y-%m-%d %H:%M'),
                'range': 'max',
            }
        
        result = ZCatalog.searchResults(self.portal_catalog, **query)
        return str(len(result))
        