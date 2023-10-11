from .views import RegisterView, LoginView, UserListAPIView, UserDetail, ChangePasswordView
from django.urls import path

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(("user/"), UserListAPIView.as_view(), name="user_personal"),
    path(("user/auth/all/"), UserListAPIView.as_view(), name="user_all"),
    path(("user/auth/pages/"), UserListAPIView.as_view(), name="user_page_all"),
    path("user/<int:pk>/", UserDetail.as_view(), name="user_detail"),
    path(("user/<int:pk>/auth/"), UserDetail.as_view(), name="user_detail_auth"),
    path(("user/auth/"), ChangePasswordView.as_view(), name="change_password"),

]