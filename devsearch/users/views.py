from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Skills, User, Message

from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.db.models import Q   # for searching in multiple fields

from .utils import searchProjects, paginationProfiles

# Create your views here.


def loginPage(request):
    page = 'login'
    context = {'page': page}
    if request.user.is_authenticated:
        return redirect('profiles')

    if(request.method == "POST"):
        username = request.POST["username"]
        password = request.POST["password"]
        print('test')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # creates a user session in the browser
            return redirect(request.GET["next"] if 'next' in request.GET else '/')
        else:
            messages.error(request, 'Username or pass incorrect')

    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request, "user logout")
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # instead of directly saving the data, we are holding the data for further modifications
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User Account was created!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'User Account was not created!')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):

    profiles, search_query = searchProjects(request)

    custom_range, profiles = paginationProfiles(request, profiles, 2)

    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skills_set.exclude(bio__exact="")
    otherSkills = profile.skills_set.filter(bio="")

    context = {'profile': profile, 'topSkills': topSkills,
               "otherSkills": otherSkills}
    context = {'profile': profile}
    return render(request, 'users/user-profile.html', context)


@login_required
def userAccount(request):
    profile = request.user.profile

    skills = profile.skills_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required
def editAccount(request):
    profile = request.user.profile

    form = ProfileForm(instance=profile)
    print(request)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    context = {'form': form}
    profile = request.user.profile
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill created!')

            return redirect('account')

    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    form = SkillForm(instance=skill)
    context = {'form': form}

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated!')

            return redirect('account')

    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted!')
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete-confirm.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    # we set the related name in message model
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    print(unreadCount, messageRequests)

    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Message sent successfully')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
