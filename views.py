#-*-encoding:UTF-8-*-
from django.http import HttpResponse
from django.template.loader import render_to_string
import os,cssutils
from django.conf import settings
import cssmanager
from django.template import RequestContext


def dirscss(request):
    if request.is_ajax():
        pathpar = request.GET.get('dir')
        rootdir=os.path.split(os.path.abspath(settings.CSSMANAGER_ROOTDIR))[0]
        if pathpar=='rootdir':
            pathpar=rootdir
        if os.path.isfile(pathpar) and os.path.exists(pathpar):
            request.session["file"] = pathpar
            #parse=cssmanager.parsecss(pathpar)
            #selectors=parse.get_selectors()
            selectors=cssmanager.get_selectors(pathpar)
            back=os.path.split(pathpar)[0]
            html = render_to_string('files.html', {'selectors': selectors,'back':back,'pathpar':pathpar,})
            return HttpResponse(html)
        elif os.path.isdir(pathpar) and pathpar.startswith(rootdir):
            if pathpar!=rootdir:
                back=os.path.split(pathpar)[0]
            else:
                back=''
            listdirs=os.listdir(pathpar)
            dirs={}
            files={}
            for name in listdirs:
                path = os.path.join(pathpar, name)
                if os.path.isfile(path) and os.path.splitext(path)[1] == '.css':
                    files[os.path.normpath(path)]=name
                elif os.path.isdir(path):
                    dirs[path]=name
            html = render_to_string('dirs.html', {'dirs': dirs,'files': files,'back': back,})
            return HttpResponse(html)
        else:
            return HttpResponse('error path')


def submitcss(request):
    if request.is_ajax():
        try:
            selector = request.GET.get('selector')
            props = request.GET.get('prop')
            dic={}
            for prop in props.split(","):
                dic[prop.split(":")[0]]=prop.split(":")[1]
            #parse=cssmanager.parsecss(request.session["file"])
            #parse.set_selectors(selector,dic)
            if cssmanager.set_selectors(request.session["file"],selector,dic)==True:
                result="Successfully saved"
            else:
                result="Problem with Saving"
            return HttpResponse(result)
        except:
            result="Saving Error"
            return HttpResponse(result)
