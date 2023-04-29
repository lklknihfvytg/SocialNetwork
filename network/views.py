from django.contrib.auth.models import User
from authentication.forms import ProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
# from messanger.models import
from .models import Profile, Photo
from posts.models import Post
from .forms import ImageForm


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

    return redirect('network:feed')


def change_path():
    profiles = Profile.objects.all()
    ex = "user/Документы/Django"
    r = "user1"
    for profile in profiles:
        s = profile.profile_pic
        if ex in s:
            profile.profile_pic = s.replace(ex, r)
            profile.save()
            print(profile.name)


def my_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    return render(request, 'profile_posts.html', {'user': request.user})


def user_profile_by_id(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'profile_posts.html', {'user': user})


def user_profile_by_username(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile_posts.html', {'user': user})


def edit_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        print(request.FILES)
        if profile_form.is_valid():
            form = profile_form.save()
            print(form)
            print('======================================')
            return render(request, 'profile_about.html', {'user': request.user})
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


def image_upload_view(request):
    if request.method == 'POST':
        print(request.FILES)
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            # photo = Photo(title=form.cleaned_data['title'], image=form.cleaned_data['image'])
            photo = Photo(title=request.POST['title'], image=request.FILES['image'])
            photo.save()
            img_obj = form.instance
            return render(request, 'photo.html', {'form': form, 'img_obj': img_obj})
        photos = Photo.objects.all()
    else:
        form = ImageForm()
        photos = Photo.objects.all()
    return render(request, 'photo.html', {'form': form, 'photos': photos})
