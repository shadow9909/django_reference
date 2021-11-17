from django.urls import path

from .views import profiles, userProfile, loginPage, logoutUser, registerUser

urlpatterns = [
    path('', profiles ,name="profiles"),
    path('logout/', logoutUser ,name="logout"),
    path('login/', loginPage ,name="login"),
    path('profile/<str:pk>/', userProfile ,name="user-profile"),
    path('register/', registerUser ,name="register"),

]

