from django.template.response import TemplateResponse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User


def about(request):
    context = {}
    return TemplateResponse(request, 'about.html', context)
