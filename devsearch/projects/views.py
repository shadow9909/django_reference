from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def projects(request):
    projects = Project.objects.all()
    context ={"projects":projects}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tag.all()
    return render(request, 'projects/single-project.html', {'project': projectObj, 'tags':tags})

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    context={'form':form}
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    form = ProjectForm(instance=Project.objects.get(id=pk))
    context={'form':form}
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES ,instance=Project.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    project=Project.objects.get(id=pk)
    context={'project':project}
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    return render(request, 'projects/delete-confirm.html', context)