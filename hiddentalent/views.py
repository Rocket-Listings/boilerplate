from django.template.response import TemplateResponse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User


def home(request):
    context = {}
    if request.user.is_authenticated():
    	return TemplateResponse(request, 'dashboard.html', context)
    else:
    	return TemplateResponse(request, 'splash.html', context)

def about(request):
    context = {}
    return TemplateResponse(request, 'about.html', context)

def styleguide(request):
	context = {}
	return TemplateResponse(request, 'style-guide.html', context)