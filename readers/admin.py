from django.contrib import admin
from .models import MyBook,Reader,Genre,Video_Review,Text_Review
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(MyBook)
admin.site.register(Reader)
admin.site.register(Genre)
admin.site.register(Text_Review)
admin.site.register(Video_Review)


class ReaderInline(admin.StackedInline):
    model = Reader
    can_delete = False
    verbose_name_plural = "reader"


class UserAdmin(BaseUserAdmin):
    inlines = (ReaderInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

