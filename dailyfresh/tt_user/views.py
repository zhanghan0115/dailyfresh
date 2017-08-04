# coding=utf-8
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from hashlib import sha1
from . import models


# Create your views here.
def register(request):
    context = {'title': '注册', 'top': '0'}
    return render(request, 'tt_user/register.html', context)


def register_handle(request):
    zhuce = request.POST
    uname = zhuce.get('user_name')
    upwd = zhuce.get('pwd')
    ucpwd = zhuce.get('cpwd')
    uemail = zhuce.get('email')
    if upwd != ucpwd:
        return redirect('/user/register/')
    s1 = sha1()
    s1.update(upwd)
    jiamipwd = s1.hexdigest()

    user_info = models.UserInfo()
    user_info.uname = uname
    user_info.upwd = jiamipwd
    user_info.uemail = uemail
    user_info.save()
    return redirect('/user/login/')


def register_valid(request):
    uname = request.GET.get('uname')
    result = models.UserInfo.objects.filter(uname=uname).count()
    context = {'valid': result}
    return JsonResponse(context)


def login(request):
    uname = request.COOKIES.get('uname')
    context = {'title': '登入', 'uanme': uname, 'top': '0'}
    return render(request, 'tt_user/login.html', context)


# def user_info(request):
#     user_info = request.POST
#     useryanzhengname = user_info.get('username')
#     useryanzhengpwd = user_info.get('pwd')
#     s1 = sha1()
#     s1.update(useryanzhengpwd)
#     jiamipwd = s1.hexdigest()
#     list = models.UserInfo.objects.filter(uname=useryanzhengname).filter(upwd=jiamipwd)
#     print list
#     if len(list)==0:
#         return render()
#     else:
#         # context={'username':useryanzhengname}
#         return render(request, 'tt_user/index.html')

def login_handle(request):
    post = request.POST
    useryanzhengname = post.get('username')
    useryanzhengpwd = post.get('pwd')
    jizhu_username = post.get('jizhu_username', '0')
    s1 = sha1()
    s1.update(useryanzhengpwd)
    jiamipwd = s1.hexdigest()
    context = {'title': '登入', 'uname': useryanzhengname, 'upwd': useryanzhengpwd, 'top': '0'}
    users = models.UserInfo.objects.filter(uname=useryanzhengname)
    if len(users) == 0:
        context['name_error'] = '1'
        return render(request, 'tt_user/login.html/', context)
    else:
        if users[0].upwd == jiamipwd:
            request.session['uid'] = users[0].id
            request.session['uname'] = useryanzhengname
            path = request.session.get('url_path', '/')#中间件
            response = redirect(path)
            if jizhu_username == '1':
                response.set_cookie('uanme', useryanzhengname,
                                    expires=datetime.datetime.now() + datetime.timedelta(days=7))
            else:
                response.set_cookie('uname', '', max_age=-1)
            return response
        else:
            context['pwd_error'] = '1'
            return render(request, 'tt_user/login.html', context)


def user_islogin(func):
    def func1(request, *args, **kwargs):
        if request.session.has_key('uid'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/user/login/')

    return func1


@user_islogin
def user_center(request):
    user = models.UserInfo.objects.get(pk=request.session['uid'])
    context = {'title': '用户中心', 'user': user}
    return render(request, 'tt_user/user_center_info.html', context)


@user_islogin
def user_order(request):
    user = models.UserInfo.objects.get(pk=request.session['uid'])
    context = {'title': '订单中心', 'user': user}
    return render(request, 'tt_user/user_center_info.html', context)


@user_islogin
def user_site(request):
    user = models.UserInfo.objects.get(pk=request.session['uid'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '收货地址', 'user': user}
    return render(request, 'tt_user/user_center_site.html/', context)


def user_loginout(request):
    request.session.flush()
    return redirect('/user/login/')
