from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def projects(request):
    return HttpResponse('projects')

def project(request, pk):
    return HttpResponse('project'+pk)