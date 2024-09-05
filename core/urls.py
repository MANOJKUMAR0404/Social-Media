from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="home"),
    path('home/',views.home,name="home2"),
    path('settings/',views.setting,name="settings"),
    path('addpost/',views.upload,name="addpost"),
    path('upload/',views.upload,name="upload"),
    path('search/',views.search,name='search'),
    path('follow/',views.follow,name='follow'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('profile2/<str:pk>',views.profile2,name='profile2'),
    path('like-post/',views.like_post,name='like-post'),
    path('home/like-post/',views.like_post,name='like-post'),
    path("signup/",views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('logout/',views.logout,name='logout'),
    
]
