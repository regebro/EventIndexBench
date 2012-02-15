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
        
    def query_simple_index(self, site, start, end, expected):
        server_url = '%s/%s' % (self.zope_url, site)
        self.get('%s/@@benchmark_query' % server_url, 
                 [['start', start.strftime('%Y-%m-%d %H:%M')],
                  ['end', end.strftime('%Y-%m-%d %H:%M')],
                 ])
        assert '<strong>%i</strong>' % expected in self.getBody()
        
    def simple_queries(self):
        for month, days in enumerate(calendar.mdays):
            for day in range(days):
                start = datetime(2010,month,day+1,12,0)
                end = start + timedelta(10)
                if end.year == 2011:
                    end = datetime(2010, 12, 31, 12, 0)
                expected = (end-start).days
                if expected < 1:
                    break
                yield {'start': start, 'end': end, 'expected': expected}
        
    def test_event_index_simple_index(self):
        self.setBasicAuth(self.admin_id, self.admin_pwd)
        self.reindex_index('simple', ['start', 'end'])

    def test_event_index_simple_query(self):
        self.setBasicAuth(self.admin_id, self.admin_pwd)
        queries = self.simple_queries()
        for query in queries:
            self.query_simple_index('simple', **query)

    def tearDown(self):
        """Setting up test."""
        self.logd('tearDown.')

if __name__ in ('main', '__main__'):
    unittest.main()
