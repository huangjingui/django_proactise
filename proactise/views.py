from django.shortcuts import render
from django.shortcuts import redirect
from proactise import models
from proactise.form import UserForm,RegisterForm
from proactise.command import hash
import datetime
from proactise.sendmail import Sendmailn
from django.conf import settings
from django.utils import timezone

def index(request):
    pass
    return render(request, 'index.html')


def login(request):

    if request.method == "POST":

        login_form = UserForm(request.POST)

        message    = ''

        if login_form.is_valid():

            ## cleaned_data 就是读取表单返回的值，返回类型为字典dict型
            username = login_form.cleaned_data['username']

            password = login_form.cleaned_data['password']


            try:
                user = models.User.objects.get(name=username)

                if not user.has_confirmed:
                    message='该用户还未确认'
                    return render(request,'login.html',locals())

                if user.password == password:                  ## 进行密码比对，成功则跳转到index页面，失败则什么都不做

                   request.session['is_login']  = True
                   request.session['user_id']   = user.id
                   request.session['user_name'] = user.name

                   return redirect('/index/')

                else:

                   message='密码不正确'
            except:

                message='用户名不存在'

        return render(request, 'login.html',locals())


    login_form = UserForm(request.POST)

    return render(request, 'login.html',locals())



def register(request):

    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")

    if request.method == "POST":

        register_form = RegisterForm(request.POST)

        message = ""

        if register_form.is_valid():  # 获取数据

            username = register_form.cleaned_data['username']

            password1 = register_form.cleaned_data['password1']

            password2 = register_form.cleaned_data['password2']

            email = register_form.cleaned_data['email']

            sex = register_form.cleaned_data['sex']

            if password1 != password2:  # 判断两次密码是否相同

                message = "两次输入的密码不同！"

                return render(request, 'register.html', locals())

            else:

                same_name_user = models.User.objects.filter(name=username)

                if same_name_user:  # 用户名唯一

                    message = '用户已经存在，请重新选择用户名！'

                    return render(request, 'register.html', locals())


                same_email_user = models.User.objects.filter(email=email)

                if same_email_user:  # 邮箱地址唯一

                    message = '该邮箱地址已被注册,请使用别的邮箱！'

                    return render(request, 'register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User()

                new_user.name = username

                new_user.password = hash(password1)

                new_user.email = email

                new_user.sex = sex

                new_user.save()


                code      = make_confirm_string(new_user)        # 邮箱确认


                user = '360300475@qq.com'                   # 邮箱内容

                passwd = 'rqxmeujyvpwjbhjh'                 # 邮箱内容

                touser = 'huangjg@xmxu.cn'                  # 邮箱内容

                username = '监控平台'                       # 邮箱内容

                subject = '腾讯云告警信息'                  # 邮箱内容

                centent = '邮箱确认信息,请点击该链接进行确认:http://127.0.0.1:12000/confirm/?code={}'.format(code)

                toname = '执行者'                           # 邮箱内容

                senmail = Sendmailn(user, passwd, new_user.email, username, subject, centent, toname)  # 发送邮件

                senmail.sends()                                                                # 进行发送

                message = '请前往注册邮箱,进行邮件确认'

                return render(request,'confirm.html',locals())

    register_form = RegisterForm()

    return render(request, 'register.html', locals())


def make_confirm_string(user):


    code = hash(user.name)

    models.ConfirmString.objects.create(code=code, user=user,)

    return code


def user_confirm(request):

    code = request.GET.get('code', None)

    message = ''

    try:

        confirm = models.ConfirmString.objects.get(code=code)

        #print(confirm)

    except:

        message = '无效的确认请求!'

        return render(request, 'confirm.html', locals())

    c_time = confirm.c_time

    now = timezone.now()

    fulure = c_time + datetime.timedelta(settings.CONFIRM_DAYS)

    if now > fulure:

        confirm.user.delete()

        message = '您的邮件已经过期！请重新注册!'

        return render(request, 'confirm.html', locals())

    else:

        confirm.user.has_confirmed = True

        confirm.user.save()

        message = '感谢确认,请使用账户登录！'

        return render(request, 'confirm.html', locals())


def logout(request):

    if not request.session.get('is_login',None):
        ## 如果本来就没登录,也就没有登出这一说
        return redirect("/index/")
    ## 退出就是直接销毁session
    request.session.flush()
    ## 或者使用下列方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/index/')
