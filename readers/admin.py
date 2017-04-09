from django.contrib import admin
from .models import MyBook,Reader,Genre,Video_Review,Text_Review
# Register your models here.
admin.site.register(MyBook)
admin.site.register(Reader)
admin.site.register(Genre)
admin.site.register(Text_Review)
admin.site.register(Video_Review)

