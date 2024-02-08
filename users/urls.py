from django.urls import path
from .views import RegisterView,RetrieveUserView,TestView,UserProfileView,RetrieveUsersView,UpdateUserAPIView,DeleteUserAPIView,GetUserView,UpdateProfileAPIView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('test/',TestView.as_view()),
    path('profile/',UserProfileView.as_view()),
    path('users_list/',RetrieveUsersView.as_view()),
    path('update_user/<int:id>/', UpdateUserAPIView.as_view()),
    path('delete_user/<int:id>/', DeleteUserAPIView.as_view()),
    path('get_user/<int:id>/', GetUserView.as_view()),
    path('update_profile/<int:id>/', UpdateProfileAPIView.as_view()),

    
]
