from django.shortcuts import render

from .models import Profile
# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skills_set.exclude(bio__exact="")
    otherSkills = profile.skills_set.filter(bio="")

    context = {'profile': profile, 'topSkills': topSkills,
               "otherSkills": otherSkills}
    context = {'profile': profile}
    return render(request, 'users/user-profile.html', context)