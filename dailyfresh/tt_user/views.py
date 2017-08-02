#coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from hashlib import sha1
from . import models
from _mysql import *
# Create your views here.

def register(request):
    context={'title':'注册'}
    return render(request, 'tt_user/register.html',context)

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


def login(request):
    context={'title':'登入'}
    return render(request, 'tt_user/login.html',context)

def index(request):
    return render(request,'tt_user/index.html')

def user_info(request):
    userInfo = request.POST

    conn = connect(host='localhost', port=3306, user='root', password='mysql', database='dailyfresh', charset='utf8')
    cs1 = conn.cursor()
    count = cs1.execute('select uname from tt_user_userinfo')
    result = cs1.fetchall()
    if userInfo.username == result[0]:
        render(request,'tt_user/index.html')

