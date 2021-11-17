#contains helper functions
from .models import Profile, Skills
from django.db.models import Q   # for searching in multiple fields


def searchProjects(request):
    
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skills.objects.filter(name__icontains=search_query)
    
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skills__in=skills))
    
    
    return profiles, search_query