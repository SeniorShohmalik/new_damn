from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',bosh_sahifa,name='bosh_sahifa'),
    # path('echo_value',echo_value,name = 'echo'),
    path('sign/',register_user,name = 'register_user'),
    path('login/',kirish,name = 'kirish'),
    # path('echo_password/',echo_password,name='echo_pass'),
    # path('register/',akkount_ochish,name='akkount_ochish'),
    # path('register_login/',register_login,name='register_l'),
    path('register_item/',mahsulot_kiritish,name='mahsulot_kiritish'),
    path('like',yoqtirganlarga_saqlash,name='yoqtirganlarga_saqlash'),
    path('star',foydalanuvchini_baholash,name='foydalanuvchini_baholash'),
    path('like_product/',mahsulotni_baholash,name='mahsulotni_baholash'),
    # path('saved_objects/',saved,name='saved'),
    path('profile/',profile,name = 'profile'),
    path('specials/',saqlangan_mahsulotlar,name='saqlangan_mahsulotlar'),
    path('search/<str:name>',search,name = 'search'),
    path('mahsulot_egasi',mahsulot_egasi,name='seller')
    
    ]