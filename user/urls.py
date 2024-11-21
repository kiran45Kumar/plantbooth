from django.urls import path
from .views import index,login,signup, CreateUser,LoginCheck,ViewUser,DeleteUser,UpdateUser,userdashboard
from . import views
urlpatterns = [
    path('', index,name='index' ),
    path("login/",login,name='login'),
    path("signup/",signup,name='signup'),
    path("create_user/",CreateUser.as_view(),name='create_user'),
    path("login_user/",LoginCheck.as_view(),name='login_user'),
    path("view_user/",ViewUser.as_view(),name='view_user'),
    path("delete_user/",DeleteUser.as_view(),name='delete_user'),
    path("update_user/",UpdateUser.as_view(),name='update_user'),
    path('user_dashboard',userdashboard,name="user_dashboard"),
    path('logout/',views.logout,name="logout"),
]