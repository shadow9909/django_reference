from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, User

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def loginPage(request):
    page ='login'
    context = {'page': page}
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if(request.method=="POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"username doesn't exist")
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) #creates a user session in the browser
            return redirect('profiles')
        else:
            messages.error(request,'Username or pass incorrect')
        
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request,"user logout")
    return redirect('login')


def registerUser(request):
    page ='register'
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # instead of directly saving the data, we are holding the data for further modifications
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User Account was created!')
            
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'User Account was not created!')
            
        
    context = {'page': page, 'form':form}
    return render(request, 'users/login_register.html', context)

@login_required
def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

@login_required
def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skills_set.exclude(bio__exact="")
    otherSkills = profile.skills_set.filter(bio="")

    context = {'profile': profile, 'topSkills': topSkills,
               "otherSkills": otherSkills}
    context = {'profile': profile}
    return render(request, 'users/user-profile.html', context)