from django.shortcuts import render,redirect
from models import Genre,MyBook
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect
import re
from django.forms import ModelForm


# Create your views here.
first_name_re=re.compile(r"^[a-zA-Z]{1,30}$")
last_name_re=re.compile(r'^[a-zA-Z]{1,30}$')
username_re=re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
password_re= re.compile(r"^.{3,20}$")
email_re= re.compile(r"^[\S]+@[\S]+.[\S]+$")




def books_in_genre(request,genre_id):
    genre=Genre.objects.get(pk=genre_id)
    books=genre.mybook_set.all()
    return render(request,"readers/book_list.html",{'books':books})

def book_detail(request,book_id):
    book=MyBook.objects.get(pk=book_id)
    return render(request,"readers/book_detail.html",{'book':book})


def homepage(request):
    genre=Genre.objects.all()
    return render(request ,"readers/homepage.html",{"genre":genre})


def signupform(request):
    return render(request,"readers/Signupform.html",{})

def validate(f,l,e,p,c):
    error=False
    error_first_name=error_last_name=error_password=error_email=""
    if   first_name_re.match(str(f).lower())==None:
        error=True
        error_first_name="First name not valid!"
    if  last_name_re.match(l.lower())==None:
        error=True
        error_last_name="Last name not valid!"
    if  email_re.match(e.lower()) ==None:
        error=True
        error_email="Email Is Required!"
    if password_re.match(p)==None or password_re.match(c)==None  or len(p)!=len(c) :
        error=True
        if(len(p)!=len(c)):
            error_password = "Password Does not Match"
        else:
            error_password = " Invalid password!"
    if error:
        return {'error_first_name':error_first_name,
                'error_last_name':error_last_name,
               'error_email':error_email,
               'error_password':error_password}
    else:
        return True

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy("readers:homepage"))



def signup(request):
    if request.method=="POST":
        first_name=request.POST.get('firstname').strip()
        last_name=request.POST.get('lastname').strip()
        email=request.POST.get('email').strip()
        password=request.POST.get('password').strip()
        confirmpassword=request.POST.get("confirmpassword").strip()
        is_author=request.POST.get("typeuser")
        is_valid=validate(first_name,last_name,email,password,confirmpassword)
        if is_valid !=True:
            error=is_valid
            return render(request,"readers/signupform.html",{'error':error,
                                                             'first_name':first_name,
                                                             'last_name':last_name,
                                                             'email':email})
        username=str(first_name)+str(last_name)
        try:
            user=User.objects.create_user(username,password=password,first_name=first_name,last_name=last_name,email=email)
            user.save()
            login(request,user)
            return HttpResponseRedirect(reverse_lazy("readers:homepage"))
        except:
            user_exist="User Already Exists !"
            return render(request, "readers/signupform.html", {'user_exists':user_exist,
                                                             'first_name':first_name,
                                                             'last_name':last_name,
                                                             'email':email})
    else:
        return render(request,"readers/signupform.html",{})





