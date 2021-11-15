from django.urls import path
from .views import project, projects, createProject, updateProject, deleteProject

urlpatterns = [
    path('', projects, name="projects"),
    path('project/<str:pk>', project, name="project"),
    path('createProject/', createProject, name="create-project"),
    path('updateProject/<str:pk>', updateProject, name="update-project"),
    path('deleteProject/<str:pk>', deleteProject, name="delete-project"),
]
