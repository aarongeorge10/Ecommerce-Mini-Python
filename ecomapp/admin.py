from django.contrib import admin
from .models import img_up,user

# Register your models here.
@admin.register(img_up)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(user)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)