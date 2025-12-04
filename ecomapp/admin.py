from django.contrib import admin
from .models import img_up,User_reg

# Register your models here.
@admin.register(img_up)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(User_reg)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)