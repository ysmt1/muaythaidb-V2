from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserUpdateForm, ProfileUpdateForm

class LoginUser(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = 'You are now logged in!'

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successful Registration')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form':form})

@login_required
def profile_view(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'You are now logged out!')
    return redirect(reverse('index'))


            

