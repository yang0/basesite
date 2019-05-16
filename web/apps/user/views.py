# _*_coding:utf-8_*_

import logging
import time, random
import re
from hashlib import md5
from datetime import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME
from django.contrib import auth
from django.utils.http import is_safe_url
from django.conf import settings
from django.db import transaction
from django.utils.safestring import SafeString
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import Group

from apps.common.base import BaseCreateView, BaseUpdateView
from apps.utils.db import *
from apps.utils.tools import json_return, get_client_ip
from apps.common.role import *
from apps.common.common import uploadFile, getFileUri
from apps.utils.verify import check_email
from apps.utils.sendmail import send_mail_thread
from apps.user.service import *
from .models import User
from rest_framework import viewsets
from .serializers import UserSerializer

logger = logging.getLogger(__name__)



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



@require_GET
@login_required
def index(request):
    return render(request, "user/index.html", {})


def login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    '''登陆视图'''
    if request.method == "GET":
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))
        next_page = request.GET.get(redirect_field_name, "")  # 默认 next
        if next_page == "":
            next_page = reverse("index")
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = reverse("index")
        request.session['next_page'] = next_page
        email = request.GET.get("email", "")
        return render(request, "user/login.html", {"email": email})
    elif request.method == "POST":
        email = strip_tags(request.POST.get("email", '').lower().strip())
        password = request.POST.get("password").strip()
        # refer = request.POST.get("refer","")
        if email == "" or password == "":
            data = {"email": email, "msg": u'请输入用户名或密码'}
            return render(request, "user/login.html", data)
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                auth.login(request, user)
                userIp = get_client_ip(request)
                updateUserByProp({"id": user.id}, {"login_ip": userIp})
                rn = request.session.get('next_page', '')
                if rn:
                    if rn.replace("http://", "") == request.get_host() + "/":
                        return HttpResponseRedirect(rn)
                        # return HttpResponseRedirect(request.session.get('next_page',reverse("user_index", args=[request.user.nick])))

                return HttpResponseRedirect(request.session.get('next_page', reverse("user_index")))
            else:
                data = {"email": email, "msg": u'无法登录'}
                return render(request, "user/login.html", data)
        else:
            data = {"email": email, "msg": u'用户名或密码错误'}
            # messages.add_message(request,messages.INFO,_(u'用户名或密码错误'))
            return render(request, "user/login.html", data)


def logout(request):
    '''注销视图'''
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def add(request):
    """超管新增用户"""

    if request.method == "POST":
        json_data = {}
        json_data['status'] = 0
        if not (request.user.is_authenticated() and request.user.is_admin):
            json_data['info'] = "未登录或无权限！"
            return json_return(json_data)
        email = request.POST.get("email", "").strip()
        nick = request.POST.get("nick", '').strip()
        pwd = request.POST.get("pwd", "").strip()
        errorMap = {}
        if email == "":
            errorMap['email'] = "请填写邮箱！"
        elif not check_email(email):
            errorMap['email'] = "邮箱格式有误！"
        else:
            emailNum = getUserCountByProp({"email": email})
            if emailNum > 0:
                errorMap['email'] = "此用户邮箱已存在！"
        if nick == "":
            errorMap['nick'] = "请填写昵称！"
        else:
            nickNum = getUserCountByProp({"nick": nick})
            if nickNum > 0:
                errorMap['nick'] = "此用户昵称已存在！"
        if pwd == "":
            errorMap['pwd'] = "请填写密码！"
        if len(errorMap) > 0:
            json_data['info'] = "参数有误！"
            json_data['error'] = errorMap
            return json_return(json_data)
        roleId = RoleOperator()
        now = datetime.now()
        uid = insertUser(User(email=email, password=md5(pwd).hexdigest(), nick=nick, name='',
                              tel='', create_time=now))
        if uid > 0:
            user = getUserObjByProp({"id": uid})
            user.groups.add(roleId)
            json_data['status'] = 1
            json_data['info'] = 'ok'
            json_data['time'] = now.strftime('%Y-%m-%d %H:%M:%S')
            return json_return(json_data)
        json_data['info'] = "添加用户失败！"
        return json_return(json_data)

    else:
        if not (request.user.is_authenticated() and request.user.is_admin):
            return HttpResponseRedirect(reverse('login') + "?next=" + reverse("user_add"))
        rid = RoleOperator()
        userList = query_sql('select * from user where id in (select user_id from user_groups where group_id=%s)',
                             [rid])
        return render(request, "user/add.html", {"userList": userList})


def register(request):
    """注册"""
    res = {}
    if request.method == "POST":
        return _save_user(request, res)
    else:
        registerType = request.GET.get('type', '').strip()
        if not registerType in ['common', 'designer', 'decorator']:
            registerType = 'common'
        res['registerType'] = registerType
        email = request.GET.get("email", '').strip()
        if email:
            res['email'] = email
    return render(request, "user/register.html", res)


def _save_user(request, res):
    # #\$\.-!%&'\*\+=\?\^_`
    word = re.compile(u"(admin|baohua|刨花|运营|管理|系统|，|[,#!`%&'\"\-\\\\$\^*+=?\.])+")

    objMap = {}
    errorMap = {}

    email = request.POST.get('email', '').strip()
    nick = request.POST.get('nick', '').strip()
    password = request.POST.get('password', '').strip()
    repassword = request.POST.get('repwd', '').strip()

    email = strip_tags(email.lower())
    nick = strip_tags(nick)
    password = strip_tags(password)
    repassword = strip_tags(repassword)

    objMap['email'] = email
    objMap['nick'] = nick
    objMap['password'] = password
    objMap['repwd'] = repassword

    if email == "":
        errorMap['email'] = """请填写邮箱！"""
    elif not check_email(email):
        errorMap['email'] = """邮箱格式不正确！"""

    if nick == "":
        errorMap['nick'] = """请填昵称！"""
    elif len(nick) < 2 or len(nick) > 12:
        errorMap['nick'] = """昵称应为2-12个字符！"""
    elif re.search(word, nick.lower()):
        errorMap['nick'] = """昵称包含非法字符！"""

    if password == "":
        errorMap['password'] = """请填写密码！"""
    if password != repassword:
        errorMap['repwd'] = """二次密码不一致！"""

    if not 'email' in errorMap:
        count = getUserCountByProp({"email": email})
        if count > 0:
            errorMap['email'] = """邮箱已存在！"""
    if not 'nick' in errorMap:
        count = getUserCountByProp({"nick": nick})
        if count > 0:
            errorMap['nick'] = """昵称已存在！"""

    res['objMap'] = objMap
    res['errorMap'] = errorMap
    # return render(request,"user/register.html",res)
    if len(errorMap) == 0:
        with transaction.commit_on_success():

            userIp = get_client_ip(request)
            userObj = User(email=email, nick=nick, password=md5(password).hexdigest(), reg_ip=userIp, login_ip=userIp,
                           name='', tel='')

            userId = insertUser(userObj)
            if not userId > 0:
                res['add_error'] = "新增用户失败！"
                return render(request, "user/register.html", res)

            user = authenticate(username=email, password=password)
            if not user is None:
                # time_str = str(time.time())
                # email = str(email)
                # chk = md5(email + "," + time_str + ",bAohuA20140507").hexdigest()
                # ver_data = email + "," + time_str + "," + chk
                # url =settings.DOMAIN + reverse('user_activate',args=[urlsafe_b64encode(ver_data),])
                # msg = u"尊敬的刨花笔记用户，" + email + u"：<br />&nbsp;&nbsp;您好！ <br />&nbsp;&nbsp;请点击以下链接激活您的账号：<br /><a href='" + url + "'>" + url + "</a>"\
                #     u"<br /><br />刨花笔记——我们为您提供贴心的分享服务！"
                # subject = '请激活帐号完成注册!'
                # from_email = '刨花笔记 <noreply@baohuabiji.com>'
                # try:
                #     send_mail_thread(subject,msg,from_email,[email],html=msg)
                #     logger.info(u"发送认证邮件==>%s",email)
                # except Exception as e:
                #     logger.error(u"发送邮箱认证邮件出错:%s",e)

                # return HttpResponseRedirect(reverse('user_email_auth')+'?email='+email)
                auth.login(request, user)
                return HttpResponseRedirect(reverse('user_success'))

            else:
                res['add_error'] = "注册失败，请重试！"
                return render(request, "user/register.html", res)

        res['add_error'] = "注册用户失败！"

    return render(request, "user/register.html", res)


@require_GET
def email_auth(request):
    email = request.GET.get('email', '').strip()
    res = {}
    if email and isinstance(email, unicode) and check_email(email):
        try:
            email = email.strip().strip('\t').strip('\n').strip('\r').strip('\0').strip('\x0B')
        except Exception as e:
            email = ''
            logger.debug("%s", e)
        email_suffix = email.split('@')[1]
        email_login = 'http://mail.' + email_suffix
        user = getUserObjByProp({"email": email})
        if user:
            if user.is_active:
                if not user.email_verify:
                    res['email'] = email
                    res['email_login'] = email_login
                else:
                    res['info'] = "该邮箱帐号已通过认证！"
            else:
                res['error'] = "该邮箱帐号已被封禁，暂时无法认证！"
        else:
            res['error'] = "该邮箱不不存在！"
    else:
        res['error'] = "认证的邮箱不存在或格式错误！"
    return render(request, "user/email_auth.html", res)


@require_GET
def activate(request, ver_data):
    """用户邮箱认证"""
    res = {}
    if ver_data:
        now = time.time()
        active_time = datetime.now()
        ver_data = urlsafe_b64decode(str(ver_data)).split(',')
        if len(ver_data) == 3:
            email = ver_data[0]
            time_str = ver_data[1]
            md5_str = ver_data[2]
            chk = md5(email + "," + time_str + ",bAohuA20140507").hexdigest()
            if md5_str == chk:
                if float(time_str) + 24 * 3600 > now:
                    user = getUserObjByProp({"email": email})
                    if user:
                        if user.is_active:
                            if not user.email_verify:
                                result = updateUserByProp({"email": email},
                                                          {"email_verify": True, "email_verify_time": active_time})
                                if result:
                                    res['success'] = "邮箱验证成功！"
                                else:
                                    res['error'] = "邮箱验证失败！"
                            else:
                                res['success'] = "该邮箱已经经过验证了！"
                        else:
                            res['error'] = "该邮箱帐号已被封禁，暂时无法验证！"
                    else:
                        res['error'] = """该邮箱帐号不存在！"""
                else:
                    res['error'] = """认证链接已失效！请重新获取认证邮件！"""
            else:
                res['error'] = """认证链接无效！"""
        else:
            res['error'] = """认证链接错误！"""
    else:
        res['error'] = """认证链接无效,err01！"""
    return render(request, "user/activate.html", res)


@login_required
def info(request):
    """个人信息"""
    res = {}
    objMap = {}
    action = 'edit'
    emailList = request.user.email.split("@")
    objMap['email'] = emailList[0][0:2] + "***@" + emailList[1]
    objMap['nick'] = request.user.nick
    if request.method == "POST":

        data = {}
        objMap['tel'] = request.POST.get("tel", '').strip()
        data['tel'] = objMap['tel']

        objMap['name'] = request.POST.get("name", "").strip()
        data['name'] = objMap['name']
        result = updateUserByProp({"id": request.user.id}, data)
        if result:
            res['status'] = 1
            res['msg'] = "修改个人资料成功"
        else:
            res['status'] = 0
            res['msg'] = "修改个人资料失败"
        res['action'] = action
        res['objMap'] = objMap
        return render(request, "user/info.html", res)
    else:
        action = request.GET.get('action', '')
        objMap['tel'] = request.user.tel
        objMap['name'] = request.user.name
        res['action'] = action

        res['objMap'] = objMap

        return render(request, "user/info.html", res)


@login_required
def chpasswd(request):
    """修改密码"""
    if request.method == "POST":
        oldPwd = request.POST.get("oldpwd", "")
        pwd = request.POST.get("password", "")
        repwd = request.POST.get("repassword", "")
        status = 1
        code = 0
        oldMsg = 0
        if not oldPwd:
            status = 0
            oldMsg = 1
        if not pwd:
            status = 0
            pwd = 0
        elif repwd != pwd:
            status = 0
            repwd = 0
        if status:
            user_obj = getUserObjByProp({"id": request.user.id})
            if md5(oldPwd).hexdigest() == user_obj.password:
                user_pwd = updateUserByProp({"id": user_obj.id}, {"password": md5(pwd).hexdigest()})
                if user_pwd:
                    code = 1
            else:
                oldMsg = 2

        if oldMsg > 0:
            oldMsg = oldMsg
        else:
            oldMsg = ''
        t_var = {
            'pwd': pwd,
            'repwd': repwd,
            'code': code,
            'oldMsg': oldMsg,
        }
        return render(request, "user/change_pwd.html", t_var)

    return render(request, "user/change_pwd.html", {})


def find_pwd(request):
    """找回密码"""
    step = 1
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        if email:
            code = 0
            try:
                user_obj = get_object_or_404(User, email=email)
                if user_obj.id:
                    time_str = str(time.time())
                    chk = md5(email + "," + time_str + ",20140507baOhua").hexdigest()
                    data = email + "," + time_str + "," + chk
                    url = settings.DOMAIN + reverse('user_reset_pwd', args=[urlsafe_b64encode(data), ])
                    msg = u"尊敬的刨花笔记用户，" + email + u"<br />&nbsp;&nbsp;您好！<br/>&nbsp;&nbsp;请点击以下链接重置密码：<br/><a href='" + url + "'>" + url + "</a>"
                    from_email = '刨花笔记 <noreply@baohuabiji.com>'
                    subject = "刨花笔记 用户密码重置提示函"
                    try:
                        send_mail_thread(subject, msg, from_email, [email], html=msg)
                        logger.info("rest password:%s", email)
                        code = 1
                        step = 2
                    except Exception as e:
                        logger.debug("rest password:%s", e)
                        code = 2
                else:
                    code = 0
                t_var = {'step': step, 'code': code, }
                return render(request, "user/find_pwd.html", t_var)
            except Exception as e:
                logger.debug("%s", e)
                t_var = {'step': step, 'code': code, }
                return render(request, "user/find_pwd.html", t_var)
        else:
            t_var = {'step': step, }
            return render(request, "user/find_pwd.html", t_var)
    else:
        t_var = {'step': step, }
        return render(request, "user/find_pwd.html", t_var)


@require_GET
def reset_pwd(request, verify):
    if verify:
        now = time.time()
        verifyList = urlsafe_b64decode(str(verify)).split(',')
        if len(verifyList) != 3:
            messages.add_message(request, messages.INFO, _(u'链接错误'))
            return render(request, "user/reset_pwd.html", {})
        email = verifyList[0]
        time_str = verifyList[1]
        md5_str = verifyList[2]
        chk = md5(email + "," + time_str + ",20140507baOhua").hexdigest()
        if md5_str == chk:
            if float(time_str) + 24 * 3600 > now:
                chkcode = md5(email + "maq_mall").hexdigest()
                t_var = {
                    'email': email,
                    'chkcode': chkcode,
                }
                return render(request, "user/reset_pwd.html", t_var)
            else:
                t_var = {'email': email, }
                messages.add_message(request, messages.INFO, _(u'密码重置链接已经失效'))
                return render(request, "user/reset_pwd.html", t_var)
        else:
            t_var = {'email': email, }
            messages.add_message(request, messages.INFO, _(u'密码重置链接链接'))
            return render(request, "user/reset_pwd.html", t_var)
    else:
        t_var = {}
        messages.add_message(request, messages.INFO, _(u'链接非法'))
        return render(request, "user/reset_pwd.html", t_var)


@require_POST
def re_pwd(request):
    code = 0
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    repassword = request.POST.get('repassword', '')
    chkcode = request.POST.get('chkcode', '')
    if email and password and repassword and chkcode:
        email = email.strip()
        password = password.strip()
        repassword = repassword.strip()
        chkcode = chkcode.strip()
        chk = md5(email + "maq_mall").hexdigest()
        if chk == chkcode and password == repassword:
            try:
                user_pwd = User.objects.filter(email=email).update(password=md5(password).hexdigest())
                code = 1
            except Exception as e:
                logger.debug("%s", e)
                code = 2
        t_var = {
            'email': email,
            'code': code,
            'chkcode': chkcode,
        }
        return render(request, "user/re_pwd.html", t_var)


from rest_framework.views import APIView
from apps.utils.tools import json_return
from django.contrib.sessions.models import Session


class onlineUsers(APIView):
    """
    获取在线登录用户数.session是四个小时过期，所以该方式不是很实时。
    """

    def get(self, request):
        users = Session.objects.filter(expire_date__gte=datetime.now()).count()
        return json_return({'status': 1, 'users': users}, ensure_ascii=False)


online_users = onlineUsers.as_view()
