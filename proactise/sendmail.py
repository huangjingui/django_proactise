# !/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from django.core.mail import EmailMultiAlternatives

class Sendmailn():

    def __init__(self,fromuser,frompass,touser,fromname,subject,centent,toname):

        self.fromuser     = fromuser

        self.frompass     = frompass

        self.touser       = touser

        self.fromname     = fromname

        self.subject      = subject

        self.centent      = centent

        self.toname       = toname


    def sends(self):

        ret=True

        try:

            msg            = MIMEText(self.centent,'plain','utf-8')               #  括里的对应发件内容

            msg['From']    = formataddr([self.fromname,self.fromuser])            #  括号里的对应发件人邮箱昵称、发件人邮箱账号

            msg['To']      = formataddr([self.toname,self.touser])                  #  括号里的对应收件人邮箱昵称、收件人邮箱账号

            msg['Subject'] = self.subject                                      #  邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com",465)                      #  发件人邮箱中的SMTP服务器，端口是25

            server.login(self.fromuser, self.frompass)                     #  括号中对应的是发件人邮箱账号、邮箱密码

            server.sendmail(self.fromuser, [self.touser, ], msg.as_string())   #  括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件

            server.quit()

        except Exception:

            ret=False

        if ret:
            print('邮件发送成功')
        else:
            print("邮件发送失败")





if __name__=="__main__":

   user    = '360300475@qq.com'
   passwd  = 'rqxmeujyvpwjbhjh'
   touser  = 'huangjg@xmxu.cn'
   username = '监控平台'
   subject = '腾讯云'
   centent=  u'<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>'
   toname  = '执行者'

   senmail= Sendmailn(user,passwd,touser,username,subject,centent,toname)

   senmail.sends()






