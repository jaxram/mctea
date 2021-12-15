import smtplib
from passlib.hash import pbkdf2_sha256
import base64
import random
import string
import pandas as pd
import json
import datetime
import django
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserId,UserDetails,Events,EventUpdate,Registration,EventQueries
@csrf_exempt
def index(request):

    req=request.POST.get('mctea')
    print(req)
    if(req=='2022'):
        token=django.middleware.csrf.get_token(request)
        print(token)
        response=HttpResponse()
        response.headers['Csrf']=token
        print("rec")
        return response
    else:
        return HttpResponse('PAGE NOT FOUND')
@csrf_exempt
def login_validation(request):
    login=request.POST.get('login')
    mail=request.POST.get('email')
    password=request.POST.get('password')
    platform=request.POST.get('isWeb')
    #print(platform)
    #print(type(platform))
    #data=[]
    fdata={}
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
                    usertype=j['usertype']
                    enc=pbkdf2_sha256.verify(password,l)

                    if enc==True:
                        print('password true')
                        l10=UserDetails.objects.filter(userid=request.session['userid']).update(lflag=0)
                        n1=64
                        res=''.join(random.choices(string.ascii_uppercase+string.digits,k=n1))
                        #print(res)
                        fdata.update({'Status':'success'})
                        #fdata.update({'token':res})
                        fdata.update({'userid':request.session['userid']})
                        fdata.update({'usertype':usertype})
                        #data.append(fdata)
                        #print(data)
                        response = JsonResponse(fdata)
                        response.headers['X-Token'] = res
                        print('...................')
                        print(response.headers['X-Token'])
                        print(response.items())
                        if(platform=='1'):
                             l11=UserId.objects.filter(userid=request.session['userid']).update(webtoken=res)
                        elif(platform=='0'):

                            l11=UserId.objects.filter(userid=request.session['userid']).update(androidtoken=res)
                        return response
                    else:
                        print('password incorrect')
                        fdata.update({'Status':'failed'})
                        fdata.update({'token':'null'})
                        fdata.update({'userid':'null'})
                        fdata.update({'usertype':'null'})
                        return HttpResponse(json.dumps(fdata))
        else:
            return HttpResponse('email failed')
    else:
        return HttpResponse('login variable is not valid')
@csrf_exempt
def password_reset(request,token):
    req=request.POST.get('request')
    user_mail=request.POST.get('email')
    var=request.POST.get('internal')
    useid=request.POST.get('userid')
    if(var=='1'):
        data1 = datetime.datetime.now()
        t=data1.strftime("%d/%m/%y %H:%M:%S")
        print(t)
        m3=UserDetails.objects.filter(userid=useid).update(password_reset=t)
        m4=UserDetails.objects.filter(userid=useid).update(resetpwdtoken=token)
        return HttpResponse('success')
    else:
        print(user_mail)
        print(token)
        if(req=='1' and user_mail!=''):
            m1=UserId.objects.filter(email=user_mail).values()
            for data in m1:
                mail=data['email']
                uid=data['userid']
            request.session['userid']=uid
            m2=UserDetails.objects.filter(userid=uid).values()
            for data in m2:
                name=data['name']
            if(mail==user_mail):
                email_user = 'mechatronicsassociation@gmail.com'#sender email
                email_password = 'MectAssociation'#sender password
                email_send = [user_mail]#reciever _mail
                subject = 'MCTEA - Reset Password'
                msg = MIMEMultipart()
                msg['From'] = 'mechatronicsassociation@gmail.com'
                msg['To'] = ", ".join(email_send)
                msg['Subject'] = subject
                body = f"""<html>
                            <body>
                            <p>Hey,<b>{name}</b></p>
                            <p> We are reaching out to you to reset your password because you have requested to reset </p>
                            <a href="https://mechatronicsea.firebaseapp.com/#/resetPwd?token={token}">Click here to reset</a><br>
                             <p> <b>Note: </b>This link will expire in 13 hrs</p>
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
                b1=UserDetails.objects.filter(userid=uid).update(password_reset=t)
                b2=UserDetails.objects.filter(userid=uid).update(resetpwdtoken=token)
                server.quit()
                return HttpResponse('success')

            else:
                return HttpResponse('not_valid_mail')

        elif(req=='1' and user_mail==''):
            return HttpResponse('restricted access')
        else:
            pass
def password_confirm(request,token):
    print("token????:",token)
    b2=UserDetails.objects.filter(resetpwdtoken=token).values()
    for data in b2:
        uid=data['userid']
        pwd=data['password_reset']
        rtoken=data['resetpwdtoken']
    #print(pwd)
    if(pwd=="NULL" and rtoken=="NULL"):
        return HttpResponse('time_over')
    elif(rtoken=="NULL"):
         return HttpResponse('time_over')
    else:
        b1=UserDetails.objects.filter(userid=uid).values()
        for data in b1.values():
            data2 = datetime.datetime.strptime(data['password_reset'], '%d/%m/%y %H:%M:%S')
        data1 = datetime.datetime.now()
        diff =data1 - data2
        days,seconds = diff.days,diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        print (hours)
        if(hours>12):
            b1=UserDetails.objects.filter(userid=uid).update(password_reset="NULL")
            return HttpResponse('time_over')
        else:
            return HttpResponse(f'success:{uid}')
@csrf_exempt
def password_save(request):
    save=request.POST.get('save')
    token=request.POST.get('token')
    pwd=request.POST.get('pwd')
    useid=request.POST.get('userid')
    if(save=='1'):
        enc=pbkdf2_sha256.hash(str(pwd))
        u1=UserId.objects.filter(userid=useid).update(password=enc)

        return HttpResponse('success')
    else:
        pass
def excel_conversion(request):
    finaldict1={}
    req=request.GET.get('request')
    dtype=request.GET.get('dtype')
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
            m3=UserId.objects.filter(userid=use).values()
            for k in m3.values():
                mail=k['email']
                temp.update({"Email":mail})
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
        #print(df)
        if(dtype=='0'):
            p=r'/home/mctea/machuraz/static/excel/'+str(t)+r'_registered.xlsx'
            fp=p[21:]
            df.to_excel(p,index=False)
            finaldict1.update({'status':'success'})
            finaldict1.update({'message':'success'})
            finaldict1.update({'data':r'https://mctea.pythonanywhere.com/'+str(fp)})
            return HttpResponse(json.dumps(finaldict1))
        else:
            fig, ax =plt.subplots(figsize=(10,4))
            ax.axis('tight')
            ax.axis('off')
            the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
            fp=r'/home/mctea/machuraz/static/pdf/'+str(t)+r'_registered.pdf'
            fp1=fp[21:]
            pp = PdfPages(fp)
            pp.savefig(fig, bbox_inches='tight')
            pp.close()
            finaldict1.update({'status':'success'})
            finaldict1.update({'message':'success'})
            finaldict1.update({'data':r'https://mctea.pythonanywhere.com/'+str(fp1)})
            return HttpResponse(json.dumps(finaldict1))

    else:
        finaldict1.update({'status':'failed'})
        finaldict1.update({'message':'req variable verification failed'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def event_save(request):
    finaldict1={}
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    event_name=request.POST.get('eventname')
    a=request.POST.get('imgdata')
    desc=request.POST.get('desc')
    participants=request.POST.get('ppt')
    eventdate=request.POST.get('eventdate')
    posterpic=request.POST.get('posterpic')
    u5=UserId.objects.filter(userid=useid).values()
    for data in u5.values():
        if(data['webtoken']==token or data['androidtoken']==token):
            b=a[a.find(",")+1:]
            image_64_decode = base64.b64decode(b)
            c=r'/home/mctea/machuraz/static/events/'+str(event_name)+r'.jpg'
            d=c[20:]
            image_result = open(c, 'wb+') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            b1=posterpic[posterpic.find(",")+1:]
            image_64_decode = base64.b64decode(b1)
            e=r'/home/mctea/machuraz/static/events/'+str(event_name)+'_poster'+r'.jpg'
            f=e[20:]
            image_result = open(e, 'wb+') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            b3=Events(eventname=event_name,eventpic=d,description=desc,participants_per_team=participants,posterpic=f,eventdate=eventdate)
            b3.save()
            print("event added")
            finaldict1.update({'status':'success'})
            finaldict1.update({'message':'success'})
            finaldict1.update({'data':{}})
            return HttpResponse(json.dumps(finaldict1))
        else:
            finaldict1.update({'status':'error'})
            finaldict1.update({'message':'token verification failed'})
            finaldict1.update({'data':{}})
            return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def post_save(request):
    finaldict1={}
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    post_data=request.POST.get('postdata')
    event_id=request.POST.get('eventid')
    a=request.POST.get('imgdata')
    if(check(useid,token)):
        #print(a)
        li=[]
        data1 = datetime.datetime.now()
        t=data1.strftime("%d/%m/%y %H:%M:%S")
        if(post_data=='' and a==None):
            return HttpResponse('failed')
        else:
            if a==None or a=='':
                c=''
                b2=EventUpdate(userid=useid,eventid=event_id,imgdata=c,eventmessage=post_data,postedon=t)
                b2.save()
                print("post added")
                finaldict1.update({'status':'success'})
                finaldict1.update({'message':'success'})
                finaldict1.update({'data':{}})
                return HttpResponse(json.dumps(finaldict1))
            else:

                n1=8
                res=''.join(random.choices(string.ascii_uppercase+string.digits,k=n1))
                c=r'/home/mctea/machuraz/static/posts/'+str(event_id)+'_'+str(res)+r'.jpg'
                d=c[20:]
                z=EventUpdate.objects.all().values()
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
                        del i['eventmessage']
                        del i['postedon']
                        li.append(i)
                    print(li)
                    for i in li:
                        if i['imgdata']==c:
                            res=''.join(random.choices(string.ascii_uppercase+string.digits,k=n1))
                            c=r'/home/mctea/machuraz/static/posts/'+str(event_id)+'_'+str(res)+r'.jpg'
                            d=c[20:]
                        else:
                            b=a[a.find(",")+1:]
                            image_64_decode = base64.b64decode(b)
                            image_result = open(c, 'wb+') # create a writable image and write the decoding result
                            image_result.write(image_64_decode)
                            print('imagesaved')
                b4=EventUpdate(userid=useid,eventid=event_id,imgdata=d,eventmessage=post_data,postedon=t)
                b4.save()
                print("post added")
                finaldict1.update({'status':'success'})
                finaldict1.update({'message':'success'})
                finaldict1.update({'data':{}})
                return HttpResponse(json.dumps(finaldict1))
    else:
        finaldict1.update({'status':'error'})
        finaldict1.update({'message':'token verification failed'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def init_home(request):
    user={}
    finalresponse={}
    finaldict={}
    finaldict1={}
    tempdict={}
    tempdict1={}
    innerdict={}
    events=[]
    updates=[]
    visiblestatus=[]
    viewedbystatus=[]
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    u5=UserId.objects.filter(userid=useid).values()
    #print(u5)
    for data in u5.values():
        if(data['webtoken']==token or data['androidtoken']==token):
            #print('ulla')
            u1=UserId.objects.filter(userid=useid).values()
            for data in u1.values():
                email=data['email']
            u2=UserDetails.objects.filter(userid=useid).values()
            for data in u2:
                name=data['name']
                pic=data['profilepic']
                if(pic==None):
                    pic='/static/dp/defaultdp.png'
            user.update({'name':name})
            user.update({'mail':email})
            user.update({'dp':pic})
            print(user)
            e1=Events.objects.all().values()
            for data in e1.values():
                eventid=data['eventid']
                eventname=data['eventname']
                eventpic=data['eventpic']
                print('''''''')
                print(eventpic)
                des=data['description']
                participants=data['participants_per_team']
                poster=data['posterpic']
                eventdate=data['eventdate']
                tempdict1.update({'eventId':eventid})
                tempdict1.update({'eventname':eventname})
                tempdict1.update({'description':des})
                tempdict1.update({'img':eventpic})
                tempdict1.update({'participants_per_team':participants})
                tempdict1.update({'posterpic':poster})
                tempdict1.update({'eventdate':eventdate})
                e4=Registration.objects.filter(eventid=eventid).values()
                tempdict1.update({'participants_count':len(e4)})
                e3=Registration.objects.filter(eventid=data['eventid']).filter(userid=useid).values()
                if(len(e3)==0):
                     tempdict1.update({'regnStatus':0})
                else:
                    for data in e3.values():
                        tempdict1.update({'regnStatus':1})
                tempdict.update({'eventDetails':tempdict1})
                e2=EventUpdate.objects.filter(eventid=eventid).values()
                for data1 in e2:
                    e3=Registration.objects.filter(eventid=data1['eventid']).filter(userid=useid).values()
                    if(len(e3)==0):
                         pass
                    else:
                        data2 = datetime.datetime.strptime(data1['postedon'], '%d/%m/%y %H:%M:%S')
                        data3 = datetime.datetime.now()
                        print(data3)
                        diff =data3 - data2
                        days,seconds = diff.days,diff.seconds
                        hours = days * 24 + seconds // 3600
                        minutes = (seconds % 3600) // 60
                        print("|||||||||||||||||||||time||||||||||||||||||||||||")
                        print (hours)
                        if(hours<=72):
                            innerdict.update({'eventid':data1['eventid']})
                            innerdict.update({'postedon':data1['postedon']})
                            innerdict.update({'message':data1['eventmessage']})
                            innerdict.update({'imgData':data1['imgdata']})
                            innerdict.update({'time':hours})
                        else:
                            pass
                    """innerdict.update({'updateid':data1['updateid']})
                    e3=Registration.objects.filter(eventid=data1['eventid']).filter(userid=useid).values()
                    if(len(e3)==0):
                        innerdict.update({'visibility':0})
                    else:
                        innerdict.update({'visibility':1})

                    if(data1['visible_status']==1):
                        if data1['userid'] in visiblestatus:
                            pass
                        else:
                            visiblestatus.append(data1['userid'])

                    else:
                        pass
                    if(data1['viewedby_status']==0):
                         viewedbystatus.append(data1['userid'])
                    else:
                        pass
                if(len(visiblestatus)!=0):
                    innerdict.update({'visibleTo':visiblestatus})
                    updates.append(innerdict)
                if(len(viewedbystatus)!=0):
                    innerdict.update({'viewedBy':viewedbystatus})"""
                    if(len(innerdict)!=0):
                        updates.append(innerdict)
                        innerdict={}
                    else:
                        pass
                finaldict.update(tempdict)
                finaldict.update({'updates':updates})
                events.append(finaldict)
                tempdict1={}
                updates=[]
                finaldict={}
            print(events)
            finaldict1.update({'status':'success'})
            finaldict1.update({'message':'0-success'})
            finalresponse.update({'user':user})
            finalresponse.update({'events':events})
            finaldict1.update({'data':finalresponse})
            return HttpResponse(json.dumps(finaldict1))
        else:
            finaldict1.update({'status':'error'})
            finaldict1.update({'message':'token verification failed'})
            finaldict1.update({'data':{}})
            return HttpResponse(json.dumps(finaldict1))
"""var response = {
//   "user": {
//     "name": "",
//     "mail": "",
//     "dp": "",
//   },
//   "events": [
//     {
//       "eventId": 123,
//       "name": "",
//       "description": "",
//       "img": "",
//       "updates": [
//         {
//           "id": 123,
//           "postedOn": "",
//           "visibleTo": [],
//           "viewedBy": [],
//           "message": "",
//           "imgData": "",
//         },
//         {},
//         {},
//       ],
//     },
//     {},
"""
@csrf_exempt
def edit_prof(request):
    finaldict1={}
    name=request.POST.get('fullName')
    number=request.POST.get('phoneNumber')
    regno=request.POST.get('regNumber')
    altemail=request.POST.get('altEmail')
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    u5=UserId.objects.filter(userid=useid).values()
    for data in u5.values():
        if(data['webtoken']==token or data['androidtoken']==token):
            if(name!=None and name!=''):
                up1=UserDetails.objects.filter(userid=useid).update(name=name)
                print('name updated')
            if(number!=None and number!=''):
                up2=UserDetails.objects.filter(userid=useid).update(mobile=number)
                print('mobile number updated')
            if(regno!=None and regno!=''):
                up3=UserDetails.objects.filter(userid=useid).update(reg_no=regno)
                print('regno updated')
            if(altemail!=None and altemail!=''):
                up4=UserDetails.objects.filter(userid=useid).update(altemail=altemail)
                print('alternate email updated')
            finaldict1.update({'status':'success'})
            finaldict1.update({'message':'success'})
            finaldict1.update({'data':{}})
            return HttpResponse(json.dumps(finaldict1))
        else:
            finaldict1.update({'status':'error'})
            finaldict1.update({'message':'token verification failed'})
            finaldict1.update({'data':{}})
            return HttpResponse(json.dumps(finaldict1))

@csrf_exempt
def dp_update(request):
    finaldict1={}
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    a=request.POST.get('imgdata')
    u5=UserId.objects.filter(userid=useid).values()
    for data in u5.values():
        if(data['webtoken']==token or data['androidtoken']==token):
            n1=8
            res=''.join(random.choices(string.ascii_uppercase+string.digits,k=n1))
            c=r'/home/mctea/machuraz/static/dp/'+str(useid)+'_dp'+r'.jpg'
            d=c[20:]
            print(d)
            z=UserDetails.objects.all().values()
            if len(z)==0:
                b=a[a.find(",")+1:]
                image_64_decode = base64.b64decode(b)
                image_result = open(c, 'wb+') # create a writable image and write the decoding result
                image_result.write(image_64_decode)
                print('userdp saved in server')
                z1=UserDetails.objects.filter(userid=useid).update(profilepic=d)
                print('userdp updated')
            else:
                z2=UserDetails.objects.filter(userid=useid).values()
                b=a[a.find(",")+1:]
                image_64_decode = base64.b64decode(b)
                image_result = open(c, 'wb+') # create a writable image and write the decoding result
                image_result.write(image_64_decode)
                print('userdp saved in server')
                z1=UserDetails.objects.filter(userid=useid).update(profilepic=d)
                print('userdp updated')
            finaldict1.update({'status':'success'})
            finaldict1.update({'message':'success'})
            finaldict1.update({'data':{}})
            return HttpResponse(json.dumps(finaldict1))
        else:
            finaldict1.update({'status':'error'})
            finaldict1.update({'message':'token verification failed'})
            finaldict1.update({'data':{}})
            return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def init_events(request):
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    eventid=request.POST.get('eventid')
    finaldict1={}
    tempdict={}
    tempdict1={}
    querydict={}
    queries=[]
    u5=UserId.objects.filter(userid=useid).values()
    for data1 in u5.values():
        if(data1['webtoken']==token or data1['androidtoken']==token):
            e1=Events.objects.filter(eventid=eventid).values()
            for data in e1.values():
                eventid=data['eventid']
                eventname=data['eventname']
                eventpic=data['eventpic']
                desc=data['description']
                participants=data['participants_per_team']
                poster=data['posterpic']
                eventdate=data['eventdate']
                e3=Registration.objects.filter(eventid=data['eventid']).filter(userid=useid).values()
                if(len(e3)==0):
                     tempdict1.update({'regnStatus':0})
                else:
                    for data in e3.values():
                        tempdict1.update({'regnStatus':1})
                tempdict1.update({'eventId':eventid})
                tempdict1.update({'eventname':eventname})
                tempdict1.update({'description':desc})
                tempdict1.update({'img':eventpic})
                tempdict1.update({'participants_per_team':participants})
                tempdict1.update({'posterpic':poster})
                tempdict1.update({'eventdate':eventdate})
            e4=Registration.objects.filter(eventid=eventid).values()
            tempdict1.update({'participants_count':len(e4)})
            tempdict.update({'eventDetails':tempdict1})
            e2=EventQueries.objects.filter(eventid=eventid).values()
            for data in e2.values():
                querydict.update({'queryid':data['id']})
                c1=data['query'].encode('ascii').decode('unicode-escape').encode('utf-16', 'surrogatepass').decode('utf-16')
                querydict.update({'query':c1})
                querydict.update({'postedby':data['postedby']})
                querydict.update({'respondedby':data['respondedby']})
                if(data['response']!=None and data['response']!=""):
                    c2=data['response'].encode('ascii').decode('unicode-escape').encode('utf-16', 'surrogatepass').decode('utf-16')
                    querydict.update({'response':c2})
                else:
                    querydict.update({'response':data['response']})
                queries.append(querydict)
                querydict={}
            tempdict.update({'queries':queries})


            finaldict1.update({'status':'success'})
            finaldict1.update({'message':'1-success'})
            finaldict1.update({'data':tempdict})
            return HttpResponse(json.dumps(finaldict1))
        else:
            finaldict1.update({'status':'error'})
            finaldict1.update({'message':'token verification failed'})
            finaldict1.update({'data':{}})
            return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def authenticate(request):
    req=request.POST.get('request')
    if(req=='1'):
        useid=request.headers['X-User']
        token=request.headers['X-Token']
        u5=UserId.objects.filter(userid=useid).values()
        for data in u5.values():
            if(data['webtoken']==token or data['androidtoken']==token):
                return HttpResponse('1')
            else:
                return HttpResponse('0')
    else:
        return HttpResponse('0')
def check(useid,token):
    u5=UserId.objects.filter(userid=useid).values()
    for data in u5.values():
        if(data['webtoken']==token or data['androidtoken']==token):
            return True
        else:
            return False
@csrf_exempt
def init_queries(request):
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    eventid=request.POST.get('eventid')
    finaldict1={}
    tempdict={}
    tempdict1={}
    querydict={}
    queries=[]
    if(check(useid,token)):
        e1=Events.objects.filter(eventid=eventid).values()
        for data in e1.values():
            eventid=data['eventid']
            eventname=data['eventname']
            poster=data['posterpic']
            tempdict1.update({'eventId':eventid})
            tempdict1.update({'eventname':eventname})
            tempdict1.update({'posterpic':poster})
            tempdict.update({'eventDetails':tempdict1})
        e2=EventQueries.objects.filter(eventid=eventid).values()
        for data in e2.values():
            querydict.update({'queryid':data['id']})
            c1=data['query'].encode('ascii').decode('unicode-escape').encode('utf-16', 'surrogatepass').decode('utf-16')
            querydict.update({'query':c1})
            querydict.update({'postedby':data['postedby']})
            querydict.update({'respondedby':data['respondedby']})
            if(data['response']!=None and data['response']!=""):
                c2=data['response'].encode('ascii').decode('unicode-escape').encode('utf-16', 'surrogatepass').decode('utf-16')
                querydict.update({'response':c2})
            else:
                querydict.update({'response':data['response']})
            queries.append(querydict)
            querydict={}
        tempdict.update({'queries':queries})
        finaldict1.update({'status':'success'})
        finaldict1.update({'message':'2-success'})
        finaldict1.update({'data':tempdict})
        return HttpResponse(json.dumps(finaldict1))
    else:
        finaldict1.update({'status':'error'})
        finaldict1.update({'message':'token verification failed'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def raise_query(request):
    finaldict1={}
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    query1=request.POST.get('query')
    query_text=query1.encode('unicode-escape').decode('ASCII')
    eventid=request.POST.get('eventid')
    if(check(useid,token)):
        e1=EventQueries.objects.create(eventid=eventid,query=query_text,postedby=useid)
        finaldict1.update({'status':'success'})
        finaldict1.update({'message':'success'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
    else:
        finaldict1.update({'status':'error'})
        finaldict1.update({'message':'token verification failed'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def respond_query(request):
    finaldict1={}
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    query1=request.POST.get('query')
    query_response=query1.encode('unicode-escape').decode('ASCII')
    queryid=request.POST.get('queryid')
    if(check(useid,token)):
        e1=EventQueries.objects.filter(id=queryid).update(respondedby=useid,response=query_response)
        finaldict1.update({'status':'success'})
        finaldict1.update({'message':'success'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
    else:
        finaldict1.update({'status':'error'})
        finaldict1.update({'message':'token verification failed'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def register_event(request):
    finaldict1={}
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    eventid=request.POST.get('eventid')
    if(check(useid,token)):
        e1=Registration(eventid=eventid,userid=useid)
        e1.save()
        finaldict1.update({'status':'success'})
        finaldict1.update({'message':'success'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
    else:
        finaldict1.update({'status':'error'})
        finaldict1.update({'message':'token verification failed'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))

@csrf_exempt
def delete_query(request):
    finaldict1={}
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    queryid=request.POST.get('queryId')
    if(check(useid,token)):
        e1=EventQueries.objects.filter(id=queryid).delete()
        finaldict1.update({'status':'success'})
        finaldict1.update({'message':'success'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
    else:
        finaldict1.update({'status':'error'})
        finaldict1.update({'message':'token verification failed'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def unregister(request):
    finaldict1={}
    useid=request.headers['X-User']
    token=request.headers['X-Token']
    eventid=request.POST.get('eventid')
    if(check(useid,token)):
        e1=Registration.objects.filter(userid=useid).filter(eventid=eventid).delete()
        finaldict1.update({'status':'success'})
        finaldict1.update({'message':'success'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
    else:
        finaldict1.update({'status':'error'})
        finaldict1.update({'message':'token verification failed'})
        finaldict1.update({'data':{}})
        return HttpResponse(json.dumps(finaldict1))
@csrf_exempt
def excel_filter(request):
    finaldict1={}
    eventid=request.POST.get('eventid')
    datas=[]
    temp={}
    e1=Registration.objects.filter(eventid=eventid).values()
    for data in e1:
        eve=data['eventid']
        use=data['userid']
        m1=UserDetails.objects.filter(userid=use).values()
        for i in m1.values():
            name=i['name']
            reg_no=i['reg_no']
            mobile=i['mobile']
            temp.update({"Name":name,"reg_no":reg_no,"mobile":mobile})
        m3=UserId.objects.filter(userid=use).values()
        for k in m3.values():
            mail=k['email']
            temp.update({"Email":mail})
        m2=Events.objects.filter(eventid=eve).values()
        print("/////////////")
        print(m2)
        for j in m2:
            eventname=j['eventname']
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
    p=r'/home/mctea/machuraz/static/excel/'+eventname+"_"+str(t)+r'_registered.xlsx'
    fp=p[21:]
    df.to_excel(p,index=False)
    finaldict1.update({'status':'success'})
    finaldict1.update({'message':'success'})
    finaldict1.update({'data':r'https://mctea.pythonanywhere.com/'+str(fp)})
    return HttpResponse(json.dumps(finaldict1))

