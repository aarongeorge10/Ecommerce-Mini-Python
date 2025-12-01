from django.shortcuts import render,redirect
from .models import img_up,user
from django.contrib.auth import authenticate ,login as log,logout
from django.core.mail import send_mail


# Create your views here.

def home(request):
    car = img_up.objects.all()
    return render(request, "home.html", {"car": car})

def register(request):
    return render(request,"register.html")

def login(request):
    return render(request,"login.html")

def userreg(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user(name=name,email=email,phonenumber=phonenumber,username=username,password=password).save()
    return render(request,'register.html')

def userlog(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        cr = user.objects.filter(username=username,password=password)
        if cr:
            user_details = user.objects.get(username=username,password=password)
            id=user_details.id
            name=user_details.name
            email=user_details.email

            request.session['id']=id
            request.session['name']=name
            request.session['email']=email

            send_mail(
                "Login", #subject
                "login successfully completed", #message
                "marzellousgaming@gmail.com",
                [email],
                fail_silently =False,
            )

            return redirect('userdashb')
        else:
            return render(request,'login.html',{'error':'Incorrect Username or Password'})       
    else:
        return render(request,'home.html')
    
def userdashb(request):
    id = request.session['id']
    name = request.session['name']
    car = img_up.objects.all()
    return render(request,"userdashb.html",{'id':id,'name':name,'car':car})


def userlogout(request):
    logout(request)
    return redirect('login')
