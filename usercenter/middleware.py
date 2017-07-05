import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse


class LoginCheck(MiddlewareMixin):
    def process_request(self, request):
        rpath = request.path
        res = re.match(r'/user(\d+)/info/$', rpath)
        if res:
            uid = request.COOKIES.get('login_id')
            if uid:  # 如果当前请求的用户中心和登录的用户不是一个，则返回已登录的用户中心
                if res.group(1) != str(uid):
                    return redirect(reverse('usercenter:user_info', args=(int(uid),)))
            else:  # 如果当前用户没有登录，则返回到登录界面
                return redirect(reverse('usercenter:login'))
