from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import (render, render_to_response, get_object_or_404)
from django.utils import simplejson as json
from django.template import RequestContext
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from BeautifulSoup import BeautifulSoup
import urllib2

def home(request):
    context = RequestContext(request)
    return render_to_response("home.html",context)

def get_url(request):
    url = request.POST.get('url')
    validate = URLValidator(verify_exists=True)
    data={}
    try:
        validate(url)
        content = urllib2.urlopen(url)
        soup = BeautifulSoup(content)
        data['title'] = soup.find("title").string
        imgs = soup.findAll("img",{"width":True})
        imgslist,width,height = [],0,0
        for i in imgs:
            print i
            width = int(i["width"])
            print width
            if width > 200:
                imgslist.append(i["src"])
        data['imgs'] = imgslist[0]
        print imgslist
        return HttpResponse(json.dumps(dict(code=1,content=data)))
    except ValidationError, e:
        return HttpResponse(json.dumps(dict(code=0,msg="Invalid Url")))
