#-*-encoding:UTF-8-*-
from django.http import HttpResponse
from django.template.loader import render_to_string
import os
from django.conf import settings
import cssmanager
import json


# Файл-бравзер
def dirscss(request):
    if request.is_ajax():
        pathpar = request.GET.get('dir')
        #path = os.path.abspath(settings.CSSMANAGER_ROOTDIR)
        #rootdir = os.path.split(path)[0]
        # корінь нашого файл-бравзера
        rootdir = os.path.abspath(settings.CSSMANAGER_ROOTDIR)
        if pathpar == 'rootdir':
            pathpar = rootdir
        if os.path.isfile(pathpar) and os.path.exists(pathpar):
            request.session["file"] = pathpar
            selectors = cssmanager.get_selectors(pathpar)
            # шлях парент директорії
            back = os.path.split(pathpar)[0]
            result = { 'back': back, 'pathpar': pathpar, 'selectors': selectors }
            """
            html = render_to_string('files.html',
                                    {'selectors': selectors,
                                     'back': back,
                                     'pathpar': pathpar, })
            return HttpResponse(html)
            """
            data = json.dumps(result)
            return HttpResponse(data, mimetype='application/json')
        elif os.path.isdir(pathpar) and pathpar.startswith(rootdir):
            if pathpar != rootdir:
                back = os.path.split(pathpar)[0]
            else:
                back = ''
            listdirs = os.listdir(pathpar)  #
            dirs = {}
            files = {}
            for name in listdirs:
                path = os.path.join(pathpar, name)
                if os.path.isfile(path) and \
                   os.path.splitext(path)[1] == '.css':
                    files[os.path.normpath(path)] = name
                elif os.path.isdir(path):
                    dirs[path] = name
            html = render_to_string('dirs.html',
                                    {'dirs': dirs,
                                     'files': files,
                                     'back': back, })
            return HttpResponse(html)
        else:
            return HttpResponse('error path')


# обробка і передача для збереженння css
def submitcss(request):
    if request.is_ajax():
        try:
            selector = request.GET.get('selector')
            props = request.GET.get('prop')
            dic = {}
            for prop in props.split(","):
                dic[prop.split(":")[0]] = prop.split(":")[1]
            try:
                try:
                    file = request.session["file"]
                except KeyError:
                    file = None
                cssmanager.set_selectors(file, selector, dic)
                result = "Successfully saved"
            except:
                result = "Problem with Saving"
            return HttpResponse(result)
        except:
            result = "Submit Error"
            return HttpResponse(result)
