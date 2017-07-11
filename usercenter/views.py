from django.shortcuts import render, redirect, reverse, get_object_or_404
from hashlib import sha1
from usercenter.models import TTSXUser
from goods.models import GoodsInfo
import datetime
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.
def register(request):
    context = {'title': '天天生鲜 - 注册', 'top': '0', 'sectop': '0'}
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
                request.session['login_id'] = u.id  # 为了知道当前登录的用户是谁
                request.session['is_login'] = '1'  # 为了知道当前有没有用户登录
                return redirect(reverse('usercenter:user_center', args=('info',)))
            else:
                # 用户名已经存在，直接返回错误信息
                context['uname_error_msg'] = '该用户名已存在'
        except Exception as e:
            print(e)
            print('用户数据存入数据库失败！！')
    return render(request, 'usercenter/register.html', context=context)


def login(request):
    context = {'title': '天天生鲜 - 登录', 'show_error': 'False', 'uname': request.COOKIES.get('uname', ''), 'top': '0',
               'sectop': '0'}
    request.session['is_login'] = '0'
    if request.method == 'POST':
        # print(request.POST)
        uname = request.POST.get("user_name")
        upasswd = request.POST.get("user_passwd")
        is_remember = request.POST.get("is_remember")  # 没有这个键名则返回 None

        s1 = sha1()
        s1.update(upasswd.encode('utf-8'))
        upasswd_sha = s1.hexdigest()

        try:
            if TTSXUser.objects.filter(uname=uname).count() == 1:
                u = TTSXUser.objects.get(uname=uname)
                tt_upasswd = u.upasswd
                if tt_upasswd == upasswd_sha:
                    context['show_error'] = 'False'
                    ref_path = request.COOKIES.get('ref_path', '/')   # 获取跳转到登录页前的地址
                    resp = redirect(ref_path)
                    resp.delete_cookie('wids')
                    request.session['login_id'] = u.id  # 记住登录用户
                    request.session['is_login'] = '1'  # 记住登录状态
                    # resp.set_cookie('login_id', u.id, expires=datetime.datetime.now() + datetime.timedelta(days=14))
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


def user_center(request, tt_site):
    tt_uid = request.session.get('login_id', 0)
    u = get_object_or_404(TTSXUser, pk=tt_uid)
    context = {'uid': tt_uid, 'user': u, 'is_login': '1'}
    if tt_site == 'info':
        # 获取用户最近浏览的物品 id
        wids_list = request.COOKIES.get('wids', '').split(',')
        if '' in wids_list:
            wids_list.remove('')
        goods_looked_list = []
        for i in wids_list:
            goods_looked_list.append(get_object_or_404(GoodsInfo, pk=int(i)))
        context['goods_list'] = goods_looked_list
        context['title'] = '天天生鲜 - 用户信息'
        return render(request, 'usercenter/user_info.html', context=context)
    elif tt_site == 'order':
        context['title'] = '天天生鲜 - 用户订单'
        return render(request, 'usercenter/user_order.html', context=context)
    elif tt_site == 'addr':
        context['title'] = '天天生鲜 - 用户地址'
        return render(request, 'usercenter/user_addr.html', context=context)


def user(request):
    tt_uid = request.session.get('login_id', 0)
    u = get_object_or_404(TTSXUser, pk=tt_uid)
    context = {'title': '天天生鲜 - 用户信息', 'uid': tt_uid, 'user': u, 'is_login': '1'}
    return render(request, 'usercenter/user_center.html', context=context)


def handle(request):
    # print(request.POST, '===================================')
    res = {'is_error': '0'}
    user_shou = request.POST.get("user_shou")
    user_addr = request.POST.get("user_addr")
    user_code = request.POST.get("user_code")
    user_phone = request.POST.get("user_phone")
    if user_shou and user_addr and user_code and user_phone and user_code.isdigit() and user_phone.isdigit() and len(
            user_code) == 6 and len(user_phone) == 11:
        u = get_object_or_404(TTSXUser, pk=request.session.get('login_id'))
        u.ushou = user_shou
        u.uaddress = user_addr
        u.ucode = user_code
        u.uphone = user_phone
        u.save()
        res['ushou'] = user_shou
        res['uaddr'] = user_addr
        res['ucode'] = user_code
        res['uphone'] = user_phone
    else:
        res['is_error'] = '1'
    return JsonResponse(res)
