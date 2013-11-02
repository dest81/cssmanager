#-*-encoding:UTF-8-*-
import os
import cssutils
import cssmanager
from django.utils import unittest
from django.test.client import Client
from django.conf import settings
from django.template import Template, Context, TemplateSyntaxError


class AjaxTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_dirscss(self):
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        # Неіснуючий файл
        file = os.path.join(settings.STATIC_ROOT, 'css\\test1.css')
        link = '/cssmanager/dirscss/?dir=' + file
        response = self.client.get(link, **kwargs)
        self.assertEqual(response.status_code, 200)

        # Корінь бравзера при запускові
        link = '/cssmanager/dirscss/?dir=rootdir'
        response = self.client.get(link, **kwargs)
        self.assertEqual(response.status_code, 200)

        # Некоренева директорія
        dir = os.path.join(settings.STATIC_ROOT, 'css')
        link = '/cssmanager/dirscss/?dir=' + dir
        response = self.client.get(link, **kwargs)
        self.assertEqual(response.status_code, 200)

        # Файл
        file = os.path.join(settings.STATIC_ROOT, 'css\\test.css')
        link = '/cssmanager/dirscss/?dir=' + file
        response = self.client.get(link, **kwargs)
        self.assertEqual(response.status_code, 200)

        link = '/cssmanager/submitcss/?selector=&prop='
        response = self.client.get(link, **kwargs)
        self.assertEqual(response.status_code, 200)


class SubmitTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        file = os.path.join(settings.STATIC_ROOT, 'css\\test.css')
        self.client.session['file'] = file
        link = '/cssmanager/submitcss/?selector=body&prop=color%3A%23333333'
        response = self.client.get(link, **kwargs)
        self.assertEqual(response.status_code, 200)


class TemplateTagTest(unittest.TestCase):
    def test_templatetag_css(self):
        t = Template("{% load cssmanager %}""{% cssmanager_css %}")
        c = Context()
        self.assertIsNotNone(t.render(c))
        #self.assertEqual(t.render(c), u'<link href="/static/css/colorpicker.css" rel="stylesheet" media="screen"> \n <script src="/static/js/cssmanager.js"></script> \n <script src="/static/js/jquery.tabslideout.v1.2.js"></script> \n <script src="/static/js/colorpicker.js"></script>')

    def test_templatetag_js(self):
        t = Template("{% load cssmanager %}""{% cssmanager_js %}")
        c = Context()
        self.assertIsNotNone(t.render(c))


class CssFuncTest(unittest.TestCase):
    def test_css(self):
        file = os.path.join(settings.STATIC_ROOT, 'css\\test.css')
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        # Перевірка отримання селектору
        sel = cssmanager.get_selectors(file)
        self.assertEqual(sel, ['body'])

        # Зміна властивостей селектора та збереження в файл
        dic = {u'color': u'#333333', u'width': u'1903px',
               u'background-color': u'#ffffff', u'height': u'1682px'}
        cssmanager.set_selectors(file, 'body', dic)

        #sel=cssmanager.get_selectors(file)
        css = cssutils.parseFile(file)
        param = css.cssRules.item(0).style.getPropertyValue('width')
        self.assertEqual(param, '1903px')

        dic = {u'color': u'#333333', u'width': u'1203px',
               u'background-color': u'#ffffff', u'height': u'1682px'}
        cssmanager.set_selectors(file, 'body', dic)

        css = cssutils.parseFile(file)
        param = css.cssRules.item(0).style.getPropertyValue('width')
        self.assertEqual(param, '1203px')
