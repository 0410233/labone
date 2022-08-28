from django.urls import path, re_path
from . import views

# urlpatterns = [
#     #用户相关
#     path('login/', views.UserLogin.as_view(), name='user-login'),

#     re_path(r'^modify/mobile/$', views.UserWxMobileModify.as_view(), name='user-modify-mobile'),
#     re_path(r'^(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='users-detail'),
#     re_path(r'^currentUser/$', views.UserCurrentDetail.as_view(), name='user-detail-current'),
# ]

app_name = 'user'
