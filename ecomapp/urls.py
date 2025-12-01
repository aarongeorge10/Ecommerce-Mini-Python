from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('userreg/',views.userreg,name="userreg"),
    path('userlog/',views.userlog,name="userlog"),
    path('userdashb/',views.userdashb,name="userdashb"),
    path('userlogout/',views.userlogout,name="userlogout"),
]