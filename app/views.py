from django.http import HttpResponse
from django.shortcuts import render_to_response
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
        # validate url for exitence as well valid syntax
        validate(url)
        content = urllib2.urlopen(url)
        soup = BeautifulSoup(content)
        data['title'] = soup.find("title").string
        imgs = soup.findAll("img",{"width":True})
        imgslist,width,height = [],0,0
        for i in imgs:
            width = int(i["width"])
            if width > 200:
                # Only appen images larger than 200px in width
                imgslist.append(i["src"])
        # We are only taking the first image in list
        data['imgs'] = imgslist[0]
        return HttpResponse(json.dumps(dict(code=1,content=data)))
    except ValidationError, e:
        return HttpResponse(json.dumps(dict(code=0,msg="Invalid Url")))
