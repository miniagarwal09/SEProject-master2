from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    genre_name = models.CharField(max_length=30)
    genre_logo = models.ImageField(default="no_image.jpg")

    def __str__(self):
        return self.genre_name


class MyBook(models.Model):
    isbn = models.IntegerField(editable=True, primary_key=True)
    book_name = models.CharField(max_length=30)
    genre = models.ManyToManyField(Genre)
    synopsis = models.TextField(max_length=500)
    cover = models.ImageField()
    sample = models.FileField(default=None)
    author = models.CharField(max_length=30)
    added_on = models.DateField(auto_now=True)
    published_on = models.DateField(default=None)
    publisher = models.CharField(max_length=30, default="Not Provided")

    def __str__(self):
        return self.book_name + " by " + self.author


class Reader(models.Model):

    favourite_genre = models.ManyToManyField(Genre, default=None)
    about_reader = models.CharField(max_length=100, default=None)
    books_read = models.ManyToManyField(MyBook, default=None, through='ReadingDetails')
    dob = models.DateField(default=None)
    country = models.CharField(max_length=30, default=None)
    reader_profile_picture = models.FileField(default=None)

    def __str__(self):
        return self.dob


class ReadingDetails(models.Model):
    book_read_on = models.DateField(auto_now=True)
    book = models.ForeignKey(MyBook, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)

    def __str__(self):
        return self.book+" read by "+self.reader


class Text_Review(models.Model):
    review = models.CharField(max_length=30)
    reader = models.ForeignKey(Reader,on_delete=models.CASCADE)
    book = models.ForeignKey(MyBook,on_delete=models.CASCADE)
    rating = models.FloatField()
    posting_time = models.TimeField()
    posting_date = models.DateField()

    def __str__(self):
        return "Review posted by"+self.reader+"on book"+self.book


class Video_Review(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(MyBook,on_delete=models.CASCADE)
    video = models.FileField()
    youtube_link = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return "Review posted by"+self.reader+"on book"+self.book