from django.contrib.auth.models import User
from authentication.forms import ProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
# from messanger.models import
from .models import Profile
from posts.models import Post


def index(request):
    # if not request.user.is_authenticated:
    #     return render(request, 'login.html')

    # car = Car.objects.get(name='m3')
    # print(car.zavod.name)
    # zavod = Zavod.objects.get(name='bmw')
    # print(zavod.car.all())
    # for el in zavod.car.all():
    #     print(el.name)

    # post = Post.objects.get(id=1)
    # user = request.user
    # posts = Post.objects.all()
    # for post in posts:
    #     print(post.likes.all())

    # for i in range (2, 11):
    #     user = User(username=('TestUser'+str(i)), password='0000')
    #     user.save()
    #     profile = Profile(user=user, name=('Тест'+str(i)), surname='Тестович')
    #     profile.save()
    #     chat = Chat.objects.create()
    #     chat.members.add(request.user)
    #     chat.members.add(user)
    #     chat.save()
    #     message = Message(sender=user, text=('Привет тест'+str(i)), chat=chat)
    #     message.save()
    #     print(user)
    #     print(profile)
    #     print(chat)
    #     print(message)

    posts = Post.objects.all()[:20]
    return render(request, 'feed.html', {'posts': posts})


def my_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    return render(request, 'profile_posts.html', {'user': request.user})


def user_profile_by_id(request, profile_id):
    user = User.objects.get(profile__id=profile_id)
    return render(request, 'profile_posts.html', {'user': user})


def user_profile_by_username(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile_posts.html', {'user': user})


def edit_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)

        if profile_form.is_valid():
            try:
                profile = request.user.profile
                profile.name = profile_form.cleaned_data['name']
                profile.surname = profile_form.cleaned_data['surname']
                profile.about = profile_form.cleaned_data['about']
                profile.city = profile_form.cleaned_data['city']
                profile.date_of_birth = profile_form.cleaned_data['date_of_birth']
                profile.save()
            except Profile.DoesNotExist:
                profile = profile_form.save(commit=False)
                profile.user = request.user
                profile.save()
            return render(request, 'edit_profile.html', {'user': request.user})
        messages.success(request, 'Ошибка в данных')
    return render(request, 'edit_profile.html', {'user': request.user})


def feed(request):
    posts = Post.objects.all()[:20]
    return render(request, 'feed.html', {'posts': posts})


def about(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    return render(request, 'profile_about.html', {'user': request.user})


def change_theme(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    print(request.GET)
    profile = Profile.objects.get(user=request.user)
    profile.dark_theme = not profile.dark_theme
    profile.save()
    try:
        redirect_to = request.GET.get('next', '')
    except Exception:
        redirect_to = 'network:feed'

    return redirect(redirect_to)
