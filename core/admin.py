from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, Seller, Tag, Profile, Request, User
# Register your models here.

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Seller)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Request)
admin.site.register(User)