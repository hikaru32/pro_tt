import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse


# class LoginCheck(MiddlewareMixin):
#     def process_request(self, request):
#         rpath = request.path
#         res = re.match(r'/user(\d+)/(info|order|addr)/$', rpath)
#         if res:
#             uid = request.session.get('login_id', 0)
#             if uid:  # 如果当前请求的用户中心和登录的用户不是一个，则返回已登录的用户中心
#                 if res.group(1) != str(uid):
#                     return redirect(reverse('usercenter:user_center', args=(int(uid), res.group(2))))
#             else:  # 如果当前用户没有登录，则返回到登录界面
#                 return redirect(reverse('usercenter:login'))


class LoginCheck(MiddlewareMixin):
    def process_request(self, request):
        # pass
        rpath = request.path
        res = re.match(r'(^/user/(info|order|addr)/$)', rpath)
        if res:
            is_login = request.session.get('is_login', '0')
            if is_login == '0':  # 如果当前请求的用户中心和登录的用户不是一个，则返回已登录的用户中心
                print(rpath, '<<<//*'*20)
                response = redirect(reverse('usercenter:login'))
                response.set_cookie('ref_path', rpath)
                return response
