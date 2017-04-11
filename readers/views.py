from django.shortcuts import render, redirect
from models import Genre, MyBook, Reader, Text_Review
from django.core.urlresolvers import reverse_lazy,reverse
from django.contrib.auth.models import User,Permission
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
import re
from django.forms import ModelForm
from django.views.generic import CreateView
import datetime


# Create your views here.
first_name_re = re.compile(r"^[a-zA-Z]{1,30}$")
last_name_re = re.compile(r'^[a-zA-Z]{1,30}$')
username_re = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
password_re = re.compile(r"^.{3,20}$")
email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def add_review(request,book_id):
    current_user = request.user.first_name
    book = MyBook.objects.get(pk=book_id)
    return HttpResponse("Review will be added by :"+current_user+"<br>The Book is"+book.book_name)


def books_in_genre(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    books = genre.mybook_set.all()
    return render(request, "readers/book_list.html", {'books': books})


def book_detail(request, book_id):
    book = MyBook.objects.get(pk=book_id)
    try:
        book_reviews = book.text_review_set.all()
    except:
        book_reviews = ""
    try:
        book_review_by_user = request.user.reader.text_review_set.get(book=book)
    except:
         book_review_by_user = ""
    return render(request, "readers/book_detail.html", {'book': book,
                                                        'book_reviews': book_reviews,
                                                        'book_review_by_user': book_review_by_user})


def homepage(request):
    genre = Genre.objects.all()
    return render(request, "readers/homepage.html",{"genre": genre})


def signupform(request):
    return render(request, "readers/Signupform.html", {})


def validate(f, l, e, p, c):
    error = False
    error_first_name = error_last_name = error_password = error_email = ""
    if first_name_re.match(str(f).lower()) is None:
        error = True
        error_first_name = "First name not valid!"
    if last_name_re.match(l.lower())is None:
        error = True
        error_last_name = "Last name not valid!"
    if email_re.match(e.lower()) is None:
        error = True
        error_email = "Email Is Required!"
    if password_re.match(p) is None or password_re.match(c) is None or len(p) != len(c):
        error = True
        if len(p) != len(c):
            error_password = "Password Does not Match"
        else:
            error_password = " Invalid password!"
    if error:
        return {'error_first_name': error_first_name,
                'error_last_name': error_last_name,
                'error_email': error_email,
                'error_password': error_password}
    else:
        return True


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy("readers:homepage"))

def reader_profile(user,request):
    pass


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname').strip()
        last_name = request.POST.get('lastname').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        confirmpassword = request.POST.get("confirmpassword").strip()
        is_valid = validate(first_name, last_name, email, password, confirmpassword)
        print is_valid
        if is_valid !=  True:
            error = is_valid
            return render(request,"readers/signupform.html", {'error': error,
                                                              'first_name': first_name,
                                                              'last_name': last_name,
                                                              'email': email})
        username = str(first_name)+str(last_name)
        try:
            user = User.objects.create_user(username, password=password, first_name=first_name, last_name=last_name, email=email)
            user.save()
            print "Successful creation of user"
            reader = Reader.objects.create(user=user)
            print "Successful creation of reader"
            reader.save()
            print "reader saved successfully"
            login(request, user)
            print "Login Successful"

            return HttpResponseRedirect(reverse("readers:home"))
        except Exception:
            user_exist = "User Already Exists !"
            return render(request, "readers/signupform.html", {'user_exists': user_exist,
                                                               'first_name': first_name,
                                                               'last_name': last_name,
                                                               'email': email})
    else:
        return render(request, "readers/signupform.html", {})


def home(request):
    reader = request.user.reader
    text_reviews = Reader.objects.get(pk=reader.id)
    video_reviews = Reader.objects.get(pk=reader.id)
    return render(request, "readers/home.html", {'reader': reader,
                                                 'text_reviews': text_reviews,
                                                 'video_reviews': video_reviews})


class TextReviewForm(ModelForm):
    class Meta:
        model = Text_Review
        fields = ['review', 'rating']


class TextReviewView(CreateView):
    model = Text_Review
    fields = ['rating', 'review']


    def form_valid(self, form):
        form.instance.reader = self.request.user.reader
        form.instance.book = MyBook.objects.get(pk=self.kwargs['book_id'])
        form.instance.posting_date = datetime.datetime.today().date().__str__()
        form.instance.posting_time = datetime.datetime.now().time().__str__()
        return super(TextReviewView, self).form_valid(form)
