from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Project, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q   # for searching in multiple fields
from .utils import searchProjects


# Create your views here.

def projects(request):

    projects, search_query = searchProjects(request)
    context = {"projects": projects, 'search_query': search_query}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tag.all()
    return render(request, 'projects/single-project.html', {'project': projectObj, 'tags': tags})


@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile
    context = {'form': form}
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # connecting projects and user
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    context = {'form': form}
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile

    project = profile.project_set.get(id=pk)
    context = {'project': project}
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    return render(request, 'delete-confirm.html', context)
