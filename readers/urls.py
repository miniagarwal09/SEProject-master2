from django.conf.urls import url
import views
from django.contrib.auth import views as auth_views
app_name="readers"
urlpatterns=[url(r'^homepage$', views.homepage,name="homepage"),
             url(r'^signupform$',views.signupform,name="signupform"),
             url(r'^signup$',views.signup,name="signup"),
             url(r'^logout$',views.logoutview,name='logout'),
             url(r'^login/$',auth_views.login,{'template_name':"registration/login.html"},name='login'),
             url(r'^genre_books/(?P<genre_id>[0-9]+)/$',views.books_in_genre,name="books_in_genre"),
             url(r'^book_detail/(?P<book_id>[0-9]+)/$',views.book_detail,name="book_detail"),
             url(r'^book_detail/(?P<book_id>[0-9]+)/add_review$',views.add_review,name="add_review"),
             url(r'^home$', views.home, name="home"),
             url(r'^text_review/(?P<book_id>[0-9]+)$', views.TextReviewView.as_view(), name="text_review")
]