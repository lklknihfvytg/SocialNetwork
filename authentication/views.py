from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from network.models import Profile
from authentication.forms import UserForm, ProfileForm, LoginForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


def register_page(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, 'Your account has been successfully created')
            return redirect('authentication:login')
        messages.success(request, 'Your account hasnt been created')

    context = {'form': UserForm(), 'profile_form': ProfileForm()}
    return render(request, 'register.html', context)


def login_user(request):
    context = {'login_form': LoginForm()}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('network:index')
        messages.success(request, 'Error!')

    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return render(request, 'login.html')


# class RegisterView(TemplateView):
#     template_name = 'register.html'
#
#     def get(self, request, **kwargs):
#         user_form = RegisterForm()
#         context = {'user_form': user_form}
#         return render(request, 'register.html', context)
#
#     def post(self, request):
#         user_form = RegisterForm(request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             login(request, user)
#             return redirect('index')
#
#         context = {'user_form': user_form}
#         return render(request, 'register.html', context)


# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile was successfully updated!')
#             return redirect('settings:profile')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/profile_posts.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })
