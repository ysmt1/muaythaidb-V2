from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from mtdb.models import Review
from .forms import UserUpdateForm, ProfileUpdateForm

class LoginUser(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'users/login.html'
    success_message = 'You are now logged in!'

class PasswordReset(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')

class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

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

    reviews = Review.objects.filter(author=request.user).order_by('-date_created')
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'reviews': reviews
    }
    return render(request, 'users/profile.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'You are now logged out!')
    return redirect(reverse('index'))


            

