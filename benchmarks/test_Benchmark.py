import unittest
import calendar
import pytz
from datetime import datetime, timedelta
from random import random
from funkload.FunkLoadTestCase import FunkLoadTestCase

class Benchmark(FunkLoadTestCase):
    """Bootstrapping the server before tests
    """

    def setUp(self):
        """Setting up test."""
        self.logd('setUp.')
        self.zope_url = self.conf_get('main', 'url')
        self.admin_id = self.conf_get('main', 'admin_id')
        self.admin_pwd = self.conf_get('main', 'admin_pwd')
    
    def reindex_index(self, site, indexes):
        server_url = '%s/%s' % (self.zope_url, site)
        self.post('%s/portal_catalog/manage_reindexIndex' % server_url,
                  [['ids', idx] for idx in indexes])
        
    def query_simple_index(site, start, end, expected):
        pass
                  
    def test_event_index_simple_index(self):
        self.setBasicAuth(self.admin_id, self.admin_pwd)
        self.reindex_index('simple', ['start', 'end'])

    def tearDown(self):
        """Setting up test."""
        self.logd('tearDown.')

if __name__ in ('main', '__main__'):
    unittest.main()
