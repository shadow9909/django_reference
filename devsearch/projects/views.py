from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
projectList = [
    {
        'id':'1',
        'name': 'archit'
    },
    {
        'id':'2',
        'name': 'casper'
    }
]
def projects(request):
    context ={"projects":projectList}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = None 
    for i in projectList:
        if i["id"] == pk:
            projectObj = i
    return render(request, 'projects/single-project.html', {'project': projectObj})