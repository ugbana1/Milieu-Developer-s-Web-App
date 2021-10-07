from django.forms.models import ModelForm
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm,ProfileForm


# Create your views here.

def loginUser(request):
    page ='login'
    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method =="POST":
       username =request.POST['username']
       password =request.POST['password']

       try:
           user =User.objects.get(username=username)

       except:
            messages.error(request,'user do not exist')
       user =authenticate(request,username=username,password=password)

       if user is not None:
           login(request,user)
           return redirect('profiles')

       else:
           messages.error(request,"Username or password is incorrect")



    return render(request,'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request,'user logged out successfully')
    return redirect('login')


def registerUser(request):
    page ='register'
    form =CustomUserCreationForm()

    if request.method =='POST':
        form =CustomUserCreationForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.username =user.username.lower()
            user.save()

            messages.success(request,'User Account was created!')

            login(request,user)
            return redirect('edit-account')
        else:
            messages.success(request,'An error has occurred during registration!')


    context ={'page':page,'form':form }
    return render(request,'users/login_register.html',context)

def profiles(request):
    profiles = Profile.objects.all()
    context ={'profiles':profiles}


    return render(request,'users/profile.html',context)

   



def userProfile(request,pk):

    profile =Profile.objects.get(id=pk)

    topSkills =profile.skill_set.exclude(description__exact="")
    otherSkills=profile.skill_set.filter(description="")
    context ={'profile':profile,'topskills':topSkills,'otherskills':otherSkills}
    return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def userAccount(request):

    profile =request.user.profile

    skills =profile.skill_set.all()

    projects =profile.project_set.all()
    

    context ={'profile':profile,'topSkills':skills,'projects':projects}

    return render(request,'users/account.html',context)


@login_required(login_url='login')
def editAccount(request):
    profile =request.user.profile 

    form =ProfileForm(instance=profile)
    if request.method =="POST":
        form =ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context ={'form':form}
    return render(request,'users/profile-form.html',context)