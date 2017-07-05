from django.shortcuts import render, redirect, reverse, get_object_or_404
from hashlib import sha1
from usercenter.models import TTSXUser
import datetime


# Create your views here.
def register(request):
    context = {'title': '天天生鲜 - 注册', 'top': '0'}
    if request.method == 'POST':
        print(request.POST)
        try:
            uname = request.POST.get('user_name')
            if TTSXUser.objects.filter(uname=uname).count() == 0:
                # 说明该用户可以注册
                upasswd = request.POST.get('user_passwd')
                uemail = request.POST.get('user_email')

                s1 = sha1()
                s1.update(upasswd.encode('utf-8'))
                upasswd_sha = s1.hexdigest()

                u = TTSXUser.objects.create(uname=uname, upasswd=upasswd_sha, uemail=uemail)
                u.save()
                return redirect(reverse('usercenter:user_info', args=(u.id,)))
            else:
                # 用户名已经存在，直接返回错误信息
                context['uname_error_msg'] = '该用户名已存在'
        except Exception as e:
            print(e)
            print('用户数据存入数据库失败！！')
    return render(request, 'usercenter/register.html', context=context)


def login(request):
    context = {'title': '天天生鲜 - 登录', 'show_error': 'False', 'uname': request.COOKIES.get('uname',''), 'top': '0'}
    if request.method == 'POST':
        # print(request.POST)
        uname = request.POST.get("user_name")
        upasswd = request.POST.get("user_passwd")
        is_remember = request.POST.get("is_remember")    # 没有这个键名则返回 None

        s1 = sha1()
        s1.update(upasswd.encode('utf-8'))
        upasswd_sha = s1.hexdigest()

        try:
            if TTSXUser.objects.filter(uname=uname).count() == 1:
                u = TTSXUser.objects.get(uname=uname)
                tt_upasswd = u.upasswd
                if tt_upasswd == upasswd_sha:
                    context['show_error'] = 'False'
                    resp = redirect(reverse('usercenter:user_info', args=(u.id,)))
                    resp.set_cookie('login_id', u.id, expires=datetime.datetime.now() + datetime.timedelta(days=14))
                    # resp.delete_cookie('login_id')
                    if is_remember:
                        resp.set_cookie('uname', uname, expires=datetime.datetime.now() + datetime.timedelta(days=14))
                    else:
                        resp.set_cookie('uname', max_age=0)
                    return resp
            context['show_error'] = 'True'
        except Exception as e:
            context['show_error'] = 'True'
            print(e)
    return render(request, 'usercenter/login.html', context=context)


def user_info(request, tt_uid):
    # print(tt_uid)
    # print(request.path, '===========')
    context = {'title': '天天生鲜 - 用户信息'}
    u = get_object_or_404(TTSXUser, pk=tt_uid)
    context['user'] = u
    return render(request, 'usercenter/user_info.html', context=context)
