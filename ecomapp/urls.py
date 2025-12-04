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
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('usercart/', views.usercart, name='usercart'),
    path('increase/<int:product_id>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:product_id>/', views.decrease_qty, name='decrease_qty'),
    path('remove/<int:product_id>/', views.remove_item, name='remove_item')
]