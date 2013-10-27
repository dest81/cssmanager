from django.utils import unittest
from django.test.client import Client
#from findservice.settings import STATIC_ROOT
from django.conf import settings
import os,cssutils,cssmanager

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        response = self.client.get('/cssmanager/dirscss/?dir',**kwargs)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/cssmanager/submitcss/?selector=&prop=',**kwargs)
        self.assertEqual(response.status_code, 200)


class SecondTest(unittest.TestCase):
    def test_details(self):
        file=os.path.join(settings.STATIC_ROOT,'css\\test.css')
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}

        #response = self.client.get('/cssmanager/submitcss/?selector=body&prop=color%3A%23333333%2Cbackground-color%3A%23615061%2Cwidth%3A1903px%2Cheight%3A1682px',**kwargs)
        #self.assertEqual(response.status_code, 200)

        sel=cssmanager.get_selectors(file)
        self.assertEqual(sel, ['body'])

        dic={u'color': u'#333333', u'width': u'1903px', u'background-color': u'#ffffff', u'height': u'1682px'}
        cssmanager.set_selectors(file,'body',dic)

        #sel=cssmanager.get_selectors(file)
        css=cssutils.parseFile(file)
        self.assertEqual(css.cssRules.item(0).style.getPropertyValue('width'),'1903px')

        dic={u'color': u'#333333', u'width': u'1203px', u'background-color': u'#ffffff', u'height': u'1682px'}
        cssmanager.set_selectors(file,'body',dic)

        css=cssutils.parseFile(file)
        self.assertEqual(css.cssRules.item(0).style.getPropertyValue('width'),'1203px')
