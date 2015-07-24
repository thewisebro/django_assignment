from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .forms import SignupForm,LoginForm,PasswordForm, UpdateForm
def login(request):
	if request.method=="POST":
		form=LoginForm(request.POST)
		if form.is_valid() :
			data=form.cleaned_data
			user=authenticate(username=data['username'], password=['password'])
			if user is not None:
				login(request,user)
				return redirect('home')
			else:
				return redirect('login')
	else:
		form=LoginForm()
	return render(request, 'login/login.html',{'form': form})
def home(request):
	return render(request, 'login/home.html', {})	
def signout(request):
	logout(request)
	return redirect('home')
def signup(request):
	if request.method=="POST":
		form=SignupForm(request.POST)
		if form.is_valid():
			profile=form.save()
			profile.save()
			user=User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
			user.save()
			return redirect('login.views.home')
	else:
		form=SignupForm()
	return render(request, 'login/signup.html',{'form':form} )
def profile(request):
		user=get_object_or_404(Profile,username=request.user['username'])
		return render(request, 'login/profile.html', {'user': user})
def update(request):
	user=get_object_or_404(Profile,username=request.user['username'])
	if request.method=='POST':
		form=UpdateForm(request.POST)
		if form.is_valid():
			data=form.cleaned_data
			user.branch=data['branch']
			user.about=data['about']
#			user.profile_pic=data['profile_pic']
#			user.cover_pic=data['cover_pic']
			user.save()
			return redirect('home')
		else:
			return redirect('update')
	else:
		form=UpdateForm(user.__dict__)
	return render(request, 'login/update.html', {'form':form})
def changepass(request):
	
		user=get_object_or_404(Profile,username=request.user['username'])
		if request.method=="POST":
			form=PasswordForm(request.POST)
			if form.is_valid():
				if user.password==form.cleaned_data['password']:
					user.password=form.cleaned_data['new_pass']
					user.save()
					return redirect('home')
				else:
					return redirect('changepass')
			else:
				return redirect('changepass')
		else:
			form=PasswordForm()
			return render(request, 'login/change_password.html', {'form':form})
	

