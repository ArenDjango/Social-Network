from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect


from django.views.generic import RedirectView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from accounts.models import *

from django.contrib.sessions.models import Session
from django.utils import timezone

def site(request):
	user = request.user
	if user.is_authenticated:
		
		allphoto = Photo.objects.all().order_by('-dataimg')
		zayavka_list = UserProfile.objects.filter(~Q(user=user))
		context = {
			"zayavka_list": zayavka_list,
			"photos": allphoto,
		}
		return render(request, "site/site.html", context)
	else:
		raise Http404




