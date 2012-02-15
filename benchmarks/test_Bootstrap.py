import unittest
import calendar
import pytz
from datetime import datetime, timedelta
from random import random
from funkload.FunkLoadTestCase import FunkLoadTestCase

class Bootstrap(FunkLoadTestCase):
    """Bootstrapping the server before tests
    """

    def setUp(self):
        """Setting up test."""
        self.logd('setUp.')
        self.zope_url = self.conf_get('main', 'url')
        self.admin_id = self.conf_get('main', 'admin_id')
        self.admin_pwd = self.conf_get('main', 'admin_pwd')

    def create_site(self, site_id, title):
        server_url = self.zope_url
        
        params = [['site_id', site_id],
                  ['title', title],
                  ['default_language', 'en'],
                  ['setup_content:boolean', 'true'],
                  ['extension_ids:list', ['plonetheme.classic:default', 'plonetheme.sunburst:default']],
                  ['form.submitted:boolean', 'True'],
                 ]
        self.post('%s/@@plone-addsite' % server_url, params)
        
    def create_event(self, site, start, end, recurrence):
        server_url = self.zope_url
        self.get('%s/%s/events/createObject?type_name=Event' % (server_url, site), load_auto_links=False)
        params = [
                  ['title', 'Event ' + str(start)],
                  ['startDate', start.strftime('%Y-%m-%d %I:%M %p')],
                  ['endDate', end.strftime('%Y-%m-%d %I:%M %p')],
                  ['startDate_year', start.strftime('%Y')],
                  ['startDate_month', start.strftime('%m')],
                  ['startDate_day', start.strftime('%d')],
                  ['startDate_hour', start.strftime('%I')],
                  ['startDate_minute', start.strftime('%M')],
                  ['startDate_ampm', start.strftime('%p')],
                  ['endDate_year', end.strftime('%Y')],
                  ['endDate_month', end.strftime('%m')],
                  ['endDate_day', end.strftime('%d')],
                  ['endDate_hour', end.strftime('%I')],
                  ['endDate_minute', end.strftime('%M')],
                  ['endDate_ampm', end.strftime('%p')],
                  ['form.submitted', '1'],
                 ]
        self.post('%s%s' % (server_url, self.getLastUrl()), params)
        
    
    def test_create_simple_site(self):
        self.setBasicAuth(self.admin_id, self.admin_pwd)
        #self.create_site('simple', 'Simple')
        
        tz = pytz.timezone('CET')
        for month, days in enumerate(calendar.mdays):
            for day in range(days):
                self.create_event(
                    site='simple',
                    start=datetime(2010,month,day+1,0,0,0,0,tz),
                    end=datetime(2010,month,day+1,0,0,0,0,tz)+timedelta(hours=1),
                    recurrence="RRULE:FREQ=HOURLY;INTERVAL=8;COUNT=10")
        
    def test_create_realdata_site(self):
        #self.create_site('real', 'Real data')
        pass
                
    def tearDown(self):
        """Setting up test."""
        self.logd('tearDown.')

if __name__ in ('main', '__main__'):
    unittest.main()
