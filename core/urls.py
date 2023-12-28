from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.UserRegister.as_view(),name="user_register"),
    path("all_users/",views.GetAllUsers.as_view(),name="all_users"),
    path("login/",views.UserLogin.as_view(),name="user_login"),
    path("csrf_cookie/",views.GetCSRFToken.as_view(),name="csrf_token"),
    path("is_authenticated/",views.IsAuthenticated.as_view(),name="is_authenticated"),
    path("logout/",views.UserLogout.as_view(),name="logout"),
]