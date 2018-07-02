from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import (
        authenticate,
        get_user_model,
        login,
        logout,
    )
from django.db.models import Q

from .forms import *
from .models import *

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
import json
import urllib

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.views.generic import RedirectView

from django.contrib.sessions.models import Session
from django.utils import timezone


def login_view(request):
    if not request.user.is_authenticated:
        next = request.GET.get('next')
        title = "Login"
        form = UserLoginForm(request.POST or None)

        

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)

            saveuser = get_object_or_404(UserProfile, user=request.user)
            if saveuser.user_online == False:
                saveuser.user_online = True
                saveuser.save()

            if next:
                return redirect(next)
            return redirect("site/")
        return render(request, "accounts/login.html", {"form": form, "title": title})
    else:
        # zayavka_list = UserProfile.objects.filter(~Q(user=user))
        # context = {
        #     "zayavka_list": zayavka_list,
        # }
        # return render(request, "site/site.html", context)
        return redirect('site/')

def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/site/")

    context = {
        "form": form,
        "title": title,
        "buttitle": "Регистрация"
    }
    return render(request, "accounts/register.html", context)

def logout_view(request):
    saveuser = get_object_or_404(UserProfile, user=request.user)
    saveuser.save()
    if saveuser.user_online == True:
        saveuser.user_online = False
        saveuser.save()

    logout(request)
    return redirect("/")

def remfrnav(request, id=None):
    userobj = get_object_or_404(UserProfile, id=id)

    user = request.user

    d = UserProfile.objects.all()

    n = userobj.user

    user.userprofile.zayavkadruzya.remove(n)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def addfrnav(request, id=None):
    userobj = get_object_or_404(UserProfile, id=id)
    # guser = get_object_or_404(User, id=id)

    user = request.user

    d = UserProfile.objects.all()

    n = userobj.user

    user.userprofile.friends.add(n)
    userobj.friends.add(user)
    user.userprofile.zayavkadruzya.remove(n)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def profilemy(request):
    formimg = Createimg(request.POST or None, request.FILES or None)
    user = request.user

    zayavka_list = UserProfile.objects.filter(~Q(user=user))

    runaddfriendend = request.POST.get("endaddfriend")
    if runaddfriendend:
        user.userprofile.friends.add(zayavka_list)
        user.userprofile.zayavkadruzya.remove(zayavka_list)


    d = UserProfile.objects.all()
    if formimg.is_valid():
        ins = formimg.save(commit=False)
        ins.user = request.user
        ins.save()
        return redirect("/profile/")
    context = {
        "forming": formimg,
        "zayavka_list": zayavka_list,
    }

    return render(request, 'accounts/profilemy.html', context)

# editprofile
def kabinetedit(request):
    instance = get_object_or_404(UserProfile, user=request.user)
    user = request.user
    zayavka_list = UserProfile.objects.filter(~Q(user=user))
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    formimg = Editprofile(request.POST or None,request.FILES or None, instance=instance)
    if request.method == 'POST':
        if formimg.is_valid():
            instance = formimg.save(commit=False)
            instance.save()
            return redirect("/profile/")
    context = {
        'formimg': formimg,
        'zayavka_list': zayavka_list,
    }
    return render(request, 'accounts/kabedit.html', context)

def listusers(request):
    users_list = UserProfile.objects.filter(~Q(user=request.user))

    druzya = request.GET.get("q")
    if druzya:
        users_list = users_list.filter(
            Q(user__first_name__icontains=druzya)|
            Q(user__last_name__icontains=druzya)|
            Q(placework__icontains=druzya)|
            Q(city__icontains=druzya)
            ).distinct()

    context = {
            "title": "ListUser",
            "users_list": users_list,
        }
    return render(request, 'accounts/listusers.html', context)


def allchat(request):
    user = request.user
    chatstory = UserProfile.objects.filter(~Q(user=user))
    messagestory = Chat.objects.all().order_by('-datamessage')
    context = {
        "chatstory":chatstory,
        "user":user,
        "messagestory":messagestory,
    }
    return render(request, 'chat/allchat.html', context)

def deletemsg(request, id=None):
    instance = get_object_or_404(Chat, id=id)
    instance.delete()
    d = instance.id
    # перенаправление в undo страницу
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def messages(request, id=None):
    userobjchat = get_object_or_404(UserProfile, id=id)
    allmessages = Chat.objects.all()
    messagestory = Chat.objects.all().order_by('-datamessage')
    user = request.user
    n = userobjchat.user
    chatstory = UserProfile.objects.filter(~Q(user=user))
    context = {
        "allmessages": allmessages,
        "chatstory": chatstory,
        "userobjchat": userobjchat,
        "messagestory": messagestory,
    }
    return render(request, 'chat/messages.html',context)


# Chat Room
def chat(request, id=None):
    userobjchat = get_object_or_404(UserProfile, id=id)
    allmessages = Chat.objects.all()
    messagestory = Chat.objects.all().order_by('-datamessage')
    user = request.user
    n = userobjchat.user
    chatstory = UserProfile.objects.filter(~Q(user=user))
    if userobjchat.user in request.user.userprofile.messagedo.all():
        request.user.userprofile.messagedo.remove(userobjchat.user)

    context = {
        "userobjchat": userobjchat,
        "allmessages": allmessages,
        "chatstory": chatstory,
        "messagestory": messagestory,
    }
    return render(request, 'chat/chat.html', context)

# Send
def postchat(request, id=None):
    if request.method == "POST":
        userobjchat = get_object_or_404(UserProfile, id=id)
        n = userobjchat.user
        # msg = request.POST.get('chat-msg')
        msg = request.POST.get('msgbox', None)
        c = Chat.objects.create(user=request.user, message=msg, useryou=n)

        userobjchat = get_object_or_404(UserProfile, id=id)
        allmessages = Chat.objects.all()
        messagestory = Chat.objects.all().order_by('-datamessage')
        user = request.user
        n = userobjchat.user
        chatstory = UserProfile.objects.filter(~Q(user=user))
        if userobjchat.user in request.user.userprofile.messagedo.all():
            request.user.userprofile.messagedo.remove(userobjchat.user)
    

        if user not in userobjchat.messagedo.all():
            userobjchat.messagedo.add(user)

        if user not in userobjchat.allmessagesstory.all() and n not in user.userprofile.allmessagesstory.all():
            user.userprofile.allmessagesstory.add(n)
            userobjchat.allmessagesstory.add(user)

    return JsonResponse({ 'msg': msg, 'user': c.user.username, 'useryou':n.username })
    
    



def userdetail(request, id=None):
    userobj = get_object_or_404(UserProfile, id=id)
    # guser = get_object_or_404(User, id=id)

    user = request.user

    d = UserProfile.objects.all()

    n = userobj.user

    removefriend = request.POST.get("removefriendend")
    if removefriend:
        user.userprofile.friends.remove(n)
        userobj.friends.remove(user)

    removeaddfriended = request.POST.get("removeaddfriend")
    if removeaddfriended:
        user.userprofile.zayavkadruzya.remove(n)

    addfriendended = request.POST.get("addfriendend")
    if addfriendended:
        user.userprofile.friends.add(n)
        userobj.friends.add(user)
        user.userprofile.zayavkadruzya.remove(n)

    rundobfriend = request.POST.get("dobavfriend")
    if rundobfriend:
        if user in userobj.zayavkadruzya.all():
            userobj.zayavkadruzya.remove(user)
        else:
            userobj.zayavkadruzya.add(user)

    initial_data = {
        "object_id": userobj.id,
    }

    context = {
        "userobj": userobj,
        "user": user,
        "d": d,
    }
    return render(request, 'accounts/profileyou.html', context)


def photomy(request, id=None):
    user = request.user
    allphoto = Photo.objects.all().order_by('-dataimg')
    formaphoto = AddPhoto(request.POST or None, request.FILES or None)
    if formaphoto.is_valid():
        instance = formaphoto.save(commit=False)
        instance.user = request.user
        instance.save() 
    context = {
        "photos": allphoto,
        "formaphoto":formaphoto,
    }
    return render(request, 'photo/photos.html', context)

def photoyou(request, id=None):
    userph = get_object_or_404(UserProfile, id=id)
    user = userph.user
    useri = request.user
    allphoto = Photo.objects.all()
    runlikeimage = request.POST.get("runlike")
    context = {
        "userph": userph,
        "allphoto": allphoto,
    }
    return render(request, 'photo/photoyou.html', context)

def likephoto(request, id=None):
    allphoto = Photo.objects.all().order_by('-dataimg')
    instance = get_object_or_404(Photo, id=id)
    user = request.user

    if user in instance.photolike.all():
        instance.photolike.remove(user)
    else:
        instance.photolike.add(user)


    context = {
        "instance": instance,
        "allphoto":allphoto,
    }
    # return undo
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs.get("id")
        obj = get_object_or_404(Photo, id=id)
        url_ = obj.user_get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.photolike.all():
                obj.photolike.remove(user)
            else:
                obj.photolike.add(user)
        return url_

class PostLikeApiToggle(APIView):
    
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id=None, format=None):
        # id = self.kwargs.get("id")
        obj = user_get_absolute_url(Photo, id=id)
        url_ = obj.user_get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.photolike.all():
                liked = False
                obj.photolike.remove(user)
            else:
                liked = True
                obj.photolike.add(user)
            updated =  True

        data = {
            "updated":updated,
            "liked": liked
        }

        return Response(data)