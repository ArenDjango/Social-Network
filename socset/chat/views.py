from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import (
        authenticate,
        get_user_model,
        login,
        logout,
    )
from django.db.models import Q

# from .forms import *
from .models import *

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
import json
import urllib


def chated(request):
    pass
    # form = ChatForm(request.POST or None)
    # # messagerun = request.POST.get("runmessagehtml")

    # if request.method == "POST" and form.is_valid():
    #     data  = form.cleaned_data
    #     new_form = form.save()

    # return render(request, 'chat/chat.html', locals())