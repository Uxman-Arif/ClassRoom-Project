from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import *


# Create your views here.

def signup(request):  
    if request.method == 'POST':  
        username = request.POST.get('signupname')   
        email = request.POST.get('email')  
        password = request.POST.get('signuppassword') 
        userregister = User(username=username, email=email)  
        userregister.set_password(password.strip())
        userregister.save()  

        return redirect('signin')

    return render(request, 'signup.html')


def signin(request):  
    if request.method == 'POST':  
        signinname = request.POST.get('signinname')  
        signinpassword = request.POST.get('signinpassword')  

        user = User.objects.filter(username=signinname).first()  
         
        if user:  
            userauth = authenticate(username=signinname, password=signinpassword.strip())  
            if userauth:  
                login(request, userauth)  
                return redirect('/home')  
            else:  
                messages.error(request, 'Wrong Password! Try again.')  
        else:  
            messages.error(request, 'This user does not exist!')  
    
    return render(request, 'signin.html')

def logoutfnc(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def home(request):
    current_user = request.user
    googlecls = googleclass.objects.filter(instructor__username = current_user)
    google_classes = googleclass.objects.filter(classinstructor__name__username=current_user)

    context = {'instructor' : googlecls, 'students' : google_classes}
    return render(request, 'home.html', context)

@login_required(login_url='signin')
def createclass(request):
    print(request.user)
    if request.method == 'POST':
        classname = request.POST.get('classname')
        classcode = request.POST.get('classcode')
        crntuser = User.objects.get(id = request.user.id)
        googleclass.objects.create(Name = classname, code = classcode, instructor = crntuser)
        return redirect('home')

    return render(request, 'createclass.html')

@login_required(login_url='signin')
def joinclass(request):
    if request.method == 'POST':
        jclassname = request.POST.get('jclassname')
        jclasscode = request.POST.get('jclasscode')
        profilepic = request.FILES.get('profilepic')
        googlecls = googleclass.objects.filter(Name = jclassname).first()

        if googlecls is not None:
            if googlecls.code == jclasscode:
                crntuser = request.user
                
                cs = googlecls.instructor.username
                if cs.strip() == crntuser.username:
                    messages.error(request, 'A instructor cannot join same class as a student.')
                else:
                    student.objects.create(name = crntuser, profilepic = profilepic, students = googlecls)
                    return redirect('home')
            else:
                messages.error(request, 'Class Code dosnot match.')
        
        else:
            messages.error(request, 'This name of class is not exist.')

    return render(request, 'joinclass.html')


@login_required(login_url='signin')
def get_resources(request, id):
    
    global global_id
    global_id = id
    if request.method == 'POST':
        btn = request.POST.get('btns')
        if btn == 'delete':
            googleclass.objects.filter(id = id).first().delete()
            return redirect('home')
        elif btn == 'left':
            crntcls = googleclass.objects.filter(id = id).first()
            cls = student.objects.filter(name__username = request.user.username, students__Name = crntcls).first().delete()
            return redirect('home')
        elif btn == 'deletelecture':
            btnlec = request.POST.get('btnslec')
            btnmsg = request.POST.get('btnsmsg')
            googleclas = googleclass.objects.filter(id = id).first()
            classdata.objects.filter(name = googleclas, lecture = btnlec, message = btnmsg).delete()
        else:
            lecture = request.FILES.get('lecture')
            lecmsg = request.POST.get('lecmsg')
            googleclas = googleclass.objects.filter(id = id).first()
            classdata.objects.create(name = googleclas, lecture = lecture, message = lecmsg)

    gglcls = googleclass.objects.filter(id = id).first()
    classmt = gglcls.class_material.all() 
    context = {'lecture' : classmt, 'gglcls' : gglcls}
    return render(request, 'get_resources.html', context)


def upload_assignment(request, id):
    if request.method == 'POST':
        btn = request.POST.get('btns')
        if btn == 'deletelecture':
            btnlec = request.POST.get('btnslec')
            btnmsg = request.POST.get('btnsmsg')
            print(btnlec, btnmsg)
            assignment.objects.filter(content = btnlec, message = btnmsg).first().delete()
        else:
            assignmnt = request.FILES.get('assignment')
            msg = request.POST.get('message')
            stdate = request.POST.get('startdate')
            dudate = request.POST.get('duedate')
            gglcls = googleclass.objects.filter(id = id).first()
            assignment.objects.create(
                name = gglcls,
                content = assignmnt,
                message = msg,
                start_date = stdate,
                due_date = dudate,
            )
    gass = assignment.objects.filter(name__id = id)
    context = {
        'gass' : gass,
        'clsid' : id,
    }
    return render(request, 'upload_assignment.html', context)

def cls_members(request, id):
    gglcls = googleclass.objects.filter(id=id).first()
    stdnts = gglcls.classinstructor.all()
    context = {'gglcls':gglcls, 'stdnts':stdnts}
    return render(request, 'class_members.html', context)

def get_assignment(request, id):
    gglcls = googleclass.objects.filter(id=id).first()
    assin = gglcls.std_assignment.all()

    context = {'assin':assin, 'gglcls':gglcls}
    return render(request, 'get_assignment.html', context)


def std_upload_assignment(request, id, stdid):
    gglcls = googleclass.objects.filter(id=id).first()
    assin = gglcls.std_assignment.filter(id=stdid)
    assid = assignment.objects.filter(id = stdid).first()
    std = student.objects.filter(id = request.user.id).first()
    upldass = assid.upload_assignment.all()
    
    if request.method == 'POST':
        submitass = request.FILES.get('submitass')
        todaydate = datetime.now().date()
        uploadassignment.objects.create(
            name = assid,
            studentname = std,
            content = submitass,
            submission_date = todaydate,
        )
    secur = uploadassignment.objects.filter(name__id = stdid)
    

    context = {
        'assin':assin,
        'gglcls':gglcls,
        'sbass' : upldass,
        'secur': secur,
    }
    return render(request, 'std_uploadass.html', context)


def instrctr_see(request, id, stdid):
    gass = assignment.objects.filter(id = stdid)
    uass = uploadassignment.objects.filter(name__id = stdid)
    print(uass)
    context = {'gass':gass, 'upldass':uass}
    return render(request, 'instrctr_see.html', context)