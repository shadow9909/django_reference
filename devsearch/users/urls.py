from django.urls import path

from .views import inbox, profiles, userProfile, loginPage, logoutUser, registerUser, userAccount, editAccount, createSkill, updateSkill, deleteSkill, inbox, viewMessage, createMessage

urlpatterns = [
    path('', profiles, name="profiles"),
    path('logout/', logoutUser, name="logout"),
    path('login/', loginPage, name="login"),
    path('profile/<str:pk>/', userProfile, name="user-profile"),
    path('register/', registerUser, name="register"),
    path('account/', userAccount, name="account"),
    path('edit-account/', editAccount, name="edit-account"),
    path('create-skill/', createSkill, name="create-skill"),
    path('update-skill/<str:pk>/', updateSkill, name="update-skill"),
    path('delete-skill/<str:pk>/', deleteSkill, name="delete-skill"),
    path('inbox/', inbox, name="inbox"),
    path('message/<str:pk>/', viewMessage, name="message"),
    path('create-message/<str:pk>/', createMessage, name="create-message"),


]
