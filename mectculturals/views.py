import smtplib
from passlib.hash import pbkdf2_sha256
import base64
import random
import string
import pandas as pd
import json
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.shortcuts import render,HttpResponse
from .models import UserId,UserDetails,Events,EventUpdate,Post,Registration
def index(request):
    return render(request,'index.html')
def login_validation(request):
    login=request.POST.get('login')
    mail=request.POST.get('email')
    password=request.POST.get('password')

    if(login=='1'):
        g=UserId.objects.all().values()
        for i in g.values():
            j=i['email']

            if j==mail:
                k=UserId.objects.filter(email=mail).values()
                for j in k:
                    l=j['password']
                    id1=j['userid']
                    request.session['userid']=id1

                    enc=pbkdf2_sha256.verify(password,l)

                    if enc==True:
                        print('password true')
                        l10=UserDetails.objects.filter(userid=request.session['userid']).update(lflag=0)
                        return HttpResponse('Success')
                    else:
                        print('password incorrect')
                        return HttpResponse('failed')
        else:
            return HttpResponse('email failed')
    else:
        return HttpResponse('login variable is not valid')
def password_reset(request,uid,token):
    req=request.POST.get('request')
    user_mail=request.POST.get('email')
    print(user_mail)
    print(uid)
    print(token)
    if(req=='1' and user_mail!=''):
        m1=UserId.objects.filter(userid=request.session['userid']).values()
        for data in m1:
            mail=data['email']
        m2=UserDetails.objects.filter(userid=request.session['userid']).values()
        for data in m2:
            name=data['name']
        if(mail==user_mail):
            email_user = 'ramsankarscr@gmail.com'#sender email
            email_password = 'RAMJOBS@22'#sender password
            email_send = [user_mail]#reciever _mail
            subject = 'PASSWORD_RESET'
            msg = MIMEMultipart()
            msg['From'] = 'ramsankarscr@gmail.com'
            msg['To'] = ", ".join(email_send)
            msg['Subject'] = subject
            body = f"""<html>
                        <body>
                        <p>Hey,{name}</p>
                        <p> We are reaching out to you to reset your password because you have requested to reset </p>
                        <a href="https://www.google.com/password_confirm/{uid}/{token}">Click here to reset</a><br>
                        <p>Regards,</p><br>
                        <p><b>Machuraz Team</b></p><br>
                        <center><p>This is a Computer-generated email,please do not reply to this message</center>
                        </body>
                    </html>
                """
            msg.attach(MIMEText(body, 'html'))
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(email_user,email_password)
            server.sendmail(email_user,email_send,text)
            print('password reset completed')
            data1 = datetime.datetime.now()
            t=data1.strftime("%d/%m/%y %H:%M:%S")
            print(t)
            b1=UserDetails.objects.filter(userid=request.session['userid']).update(password_reset=t)
            server.quit()
            return HttpResponse('success')
        else:
            return HttpResponse('not_valid_mail')

    elif(req=='1' and user_mail==''):
        return HttpResponse('restricted access')
    else:
        pass
def password_confirm(request,uid,token):
    print(uid)
    print(token)
    b2=UserDetails.objects.filter(userid=request.session['userid']).values()
    for data in b2:
        pwd=data['password_reset']
    print(pwd)
    if(pwd=="NULL"):
        return HttpResponse('time_over')
    else:
        b1=UserDetails.objects.filter(userid=request.session['userid']).values()
        for data in b1.values():
            data2 = datetime.datetime.strptime(data['password_reset'], '%d/%m/%y %H:%M:%S')
        data1 = datetime.datetime.now()
        diff =data1 - data2
        days,seconds = diff.days,diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        print (hours)
        if(hours>12):
            b1=UserDetails.objects.filter(userid=request.session['userid']).update(password_reset="NULL")
            return HttpResponse('time_over')
        else:
            return HttpResponse('success')
def password_save(request):
    save=request.POST.get('save')
    pwd=request.POST.get('pwd')
    if(save=='1'):
        enc=pbkdf2_sha256.hash(str(pwd))
        u1=UserId.objects.filter(userid=request.session['userid']).update(password=enc)
        return HttpResponse('success')
    else:
        pass
def excel_conversion(request):
    req=request.GET.get('request')
    if(req=='1'):
        datas=[]
        temp={}
        e1=Registration.objects.all().values()
        for data in e1:
            eve=data['eventid']
            use=data['userid']
            m1=UserDetails.objects.filter(userid=use).values()
            for i in m1.values():
                name=i['name']
                reg_no=i['reg_no']
                mobile=i['mobile']
                temp.update({"Name":name,"reg_no":reg_no,"mobile":mobile})
            m2=Events.objects.filter(eventid=eve).values()
            for j in m2:
                temp.update({"event":j['eventname']})
            datas.append(temp)
            print(datas)
            print("dict appended")
            df = pd.DataFrame.from_dict(datas)
            temp={}
            print(temp)

        date1 = datetime.datetime.now()
        t=date1.strftime("%d_%m_%y_%H-%M-%S")
        print(t)
        print(df)
        df.to_excel(r'excel/'+str(t)+r'_registered.xlsx',index=False)
        return HttpResponse('success')
    else:
        pass
def event_save(request):
    req2=request.POST.get('request')
    event_name=request.POST.get('eventname')
    a=request.POST.get('imgdata')
    if req2=='1':
        if a==None or a=='NULL':
            c='NULL'
            b2=Events(eventname=event_name,eventpic=c)
            b2.save()
            print("event added")
            return HttpResponse('success')
        else:
            b=a[a.find(",")+1:]
            image_64_decode = base64.b64decode(b)
            c=r'events/'+str(event_name)+r'.jpg'
            image_result = open(c, 'wb+') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            b3=Events(eventname=event_name,eventpic=c)
            b3.save()
            print("event added")
            return HttpResponse('success')
    else:
        pass
def post_save(request):
    req2=request.POST.get('request')
    post_data=request.POST.get('postdata')
    a=request.POST.get('imgdata')
    useid=request.POST.get('userid')
    event_id=request.POST.get('eventid')
    if req2=='1':
        print(a)
        li=[]
        data1 = datetime.datetime.now()
        t=data1.strftime("%d/%m/%y %H:%M:%S")
        if(post_data=='' and a==None):
            return HttpResponse('failed')
        else:
            if a==None or a=='NULL':
                c='NULL'
                b2=Post(userid=useid,eventid=event_id,imgdata=c,postdata=post_data,posttime=t)
                b2.save()
                print("post added")
                return HttpResponse('success')
            else:

                n1=8
                res=''.join(random.choices(string.ascii_uppercase+string.digits,k=n1))
                c=r'posts/'+str(event_id)+'_'+str(res)+r'.jpg'
                z=Post.objects.all().values()
                if len(z)==0:
                    b=a[a.find(",")+1:]
                    image_64_decode = base64.b64decode(b)
                    image_result = open(c, 'wb+') # create a writable image and write the decoding result
                    image_result.write(image_64_decode)
                    print('imagesaved')
                else:
                    for i in z.values():
                        del i['eventid']
                        del i['userid']
                        del i['postdata']
                        del i['posttime']
                        li.append(i)
                    print(li)
                    for i in li:
                        if i['imgdata']==c:
                            res=''.join(random.choices(string.ascii_uppercase+string.digits,k=n1))
                            c=r'posts/'+str(event_id)+'_'+str(res)+r'.jpg'

                        else:
                            b=a[a.find(",")+1:]
                            image_64_decode = base64.b64decode(b)
                            image_result = open(c, 'wb+') # create a writable image and write the decoding result
                            image_result.write(image_64_decode)
                            print('imagesaved')
                b4=Post(userid=useid,eventid=event_id,imgdata=c,postdata=post_data,posttime=t)
                b4.save()
                print("post added")
                return HttpResponse('success')
    else:
        pass





