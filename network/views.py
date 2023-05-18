from django.contrib.auth.models import User
from django.views import View

from authentication.forms import ProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ImageForm
from .models import Profile, Photo
from posts.models import Post
from django.db.models import Q


def index(request):
    return redirect('network:feed')


class ProfilePage(View):
    template_name = 'profile_posts.html'

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except Exception:
            return redirect('network:feed')

        posts = user.posts.all()
        my_friends = user.profile.friends.all()
        friend = user.profile.user_friends.all()
        friends = my_friends & friend
        follows = my_friends.difference(friends)
        followers = friend.difference(friends)

        relation = None
        if request.user.is_authenticated:
            recs = Profile.objects.exclude(user=request.user)[:6]
            if user != request.user:
                mas = [request.user.profile.friends.filter(user__id=user_id).count(),
                       request.user.profile.user_friends.filter(user__id=user_id).count()]
                if mas == [1, 1]:
                    relation = 'friend'
                elif mas == [0, 1]:
                    relation = 'follower'
                elif mas == [1, 0]:
                    relation = 'follow'
        else:
            recs = Profile.objects.all()[:6]

        context = {
            'user': user,
            'relation': relation,
            'posts': posts,
            'friends': friends,
            'follows': follows,
            'followers': followers,
            'count': my_friends.count() + friend.count(),
            'recs': recs,
        }
        return render(request, self.template_name, context)


class ProfilePhotosView(View):
    def get(self, request, user_id):
        try:
            photos = Photo.objects.filter(user__id=user_id)
            user = User.objects.get(id=user_id)
        except Exception:
            return redirect('network:feed')

        context = {
            'photos': photos,
            'user': user
        }
        return render(request, 'profile_photos.html', context)

    def post(self, request):
        image_form = ImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image_form.save()

        return redirect('network:user_photos', user_id=request.POST['page_owner_id'])


# def user_profile_by_id(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#     except Exception:
#         return redirect('network:feed')
#
#     relation = None
#     if request.user.is_authenticated:
#         if user != request.user:
#             mas = [request.user.profile.friends.filter(user__id=user_id).count(),
#                    request.user.profile.user_friends.filter(user__id=user_id).count()]
#             if mas == [1, 1]:
#                 relation = 'friend'
#             elif mas == [0, 1]:
#                 relation = 'follower'
#             elif mas == [1, 0]:
#                 relation = 'follow'
#     context = {
#         'user': user,
#         'relation': relation
#     }
#     return render(request, 'profile_posts.html', context)
#
#
# def my_profile(request):
#     if not request.user.is_authenticated:
#         return render(request, 'login.html')
#
#     return render(request, 'profile_posts.html', {'user': request.user})
#
#
# def user_profile_by_username(request, username):
#     try:
#         user = User.objects.get(username=username)
#     except Exception:
#         return redirect('network:feed')
#
#     return redirect('network:user_profile_by_id', user_id=user.id)


def edit_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return render(request, 'profile_about.html', {'user': request.user})
        messages.success(request, 'Ошибка в данных')

    return render(request, 'edit_profile.html', {'user': request.user})


def feed(request):
    posts = Post.objects.all()[:20]
    if request.user.is_authenticated:
        recs = Profile.objects.exclude(user=request.user)[:6]
    else:
        recs = Profile.objects.all()[:6]
    return render(request, 'feed.html', {'posts': posts, 'recs': recs})


def videos(request):
    return render(request, 'my_videos.html')


def photos(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    try:
        photos = Photo.objects.filter(user__id=request.user.id)
    except Exception:
        return redirect('network:feed')

    context = {
        'photos': photos,
        'user': request.user,
    }
    return render(request, 'my_photos.html', context)

# def about(request):
#     if not request.user.is_authenticated:
#         return render(request, 'login.html')
#     return render(request, 'profile_about.html', {'user': request.user})


# def user_about(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#     except Exception:
#         return redirect('network:feed')
#
#     return render(request, 'profile_about.html', {'user': user})


def change_theme(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    profile = Profile.objects.get(user=request.user)
    profile.dark_theme = not profile.dark_theme
    profile.save()
    try:
        redirect_to = request.GET.get('next', '')
    except Exception:
        redirect_to = 'network:feed'

    return redirect(redirect_to)


# def user_friends(request, user_id):
#     if not request.user.is_authenticated:
#         return render(request, 'login.html')
#
#     try:
#         user = User.objects.get(id=user_id)
#     except Exception:
#         return redirect('network:feed')
#
#     my_friends = user.profile.friends.all()
#     friend = user.profile.user_friends.all()
#     friends = my_friends & friend
#     follows = my_friends.difference(friends)
#     followers = friend.difference(friends)
#
#     context = {
#         'user': user,
#         'friends': friends,
#         'follows': follows,
#         'followers': followers,
#         'count': my_friends.count() + friend.count()
#     }
#
#     return render(request, 'profile_friends.html', context)


def friends(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    my_friends = request.user.profile.friends.all()
    friend = request.user.profile.user_friends.all()
    friends = my_friends & friend
    follows = my_friends.difference(friends)
    followers = friend.difference(friends)
    recs = Profile.objects.exclude(user=request.user)[:6]

    context = {
        'friends': friends,
        'follows': follows,
        'followers': followers,
        'count': my_friends.count() + friend.count(),
        'recs': recs,
    }

    return render(request, 'friends.html', context)


def follow(request, user_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    friends = request.user.profile.friends
    if friends.filter(user__id=user_id).count() == 0:
        try:
            friend = Profile.objects.get(user__id=user_id)
            friends.add(friend)
        except Exception:
            return redirect('network:feed')

    return redirect('network:user_profile_by_id', user_id=user_id)


def unfollow(request, user_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    friends = request.user.profile.friends
    if friends.filter(user__id=user_id).count() == 1:
        try:
            friend = Profile.objects.get(user__id=user_id)
            friends.remove(friend)
        except Exception:
            return redirect('network:feed')

    return redirect('network:user_profile_by_id', user_id=user_id)


def search(request):
    words = request.GET['text'].split(' ')
    qs = User.objects.none()
    for word in words[:4]:
        qs = qs | User.objects.filter(
            Q(profile__name=word) | Q(profile__surname=word) | Q(username=word)
        )
    context = {
        'search': True,
        'users': qs
    }
    return render(request, 'friends.html', context)


# def user_videos(request, user_id):
#     return render(request, 'profile_videos.html')


# def image_upload_view(request):
#     if request.method == 'POST':
#         print(request.FILES)
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             # form.save()
#             # photo = Photo(title=form.cleaned_data['title'], image=form.cleaned_data['image'])
#             photo = Photo(title=request.POST['title'], image=request.FILES['image'])
#             photo.save()
#             img_obj = form.instance
#             return render(request, 'photo.html', {'form': form, 'img_obj': img_obj})
#         photos = Photo.objects.all()
#     else:
#         form = ImageForm()
#         photos = Photo.objects.all()
#     return render(request, 'photo.html', {'form': form, 'photos': photos})


def change_names():
    names = ['Александр', 'Максим', 'София', 'Михаил', 'Марк', 'Мария', 'Иван', 'Артем', 'Алиса', 'Лев',
             'Дмитрий', 'Ева', 'Матвей', 'Даниил', 'Виктория', 'Варвара', 'Александра', 'Анастасия']
    surnames = ['Иванов', 'Смирнов', 'Кузнецова', 'Попов', 'Васильев', 'Петрова', 'Соколов', 'Михайлов', 'Новикова',
                'Федоров', 'Морозов', 'Волкова', 'Алексеев', 'Лебедев', 'Семенова', 'Егорова', 'Павлова', 'Козлова']
    i = 0
    users = User.objects.all()
    print(users)
    for user in users:
        if 'Тест' in user.profile.name:
            user.profile.name = names[i]
            user.profile.surname = surnames[i]
            user.profile.save()
            user.save()
            i += 1


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


def create_users():
    for i in range (2, 11):
        user = User(username=('TestUser'+str(i)), password='0000')
        user.save()
        # profile = Profile(user=user, name=('Тест'+str(i)), surname='Тестович')
        # profile.save()
        # chat = Chat.objects.create()
        # chat.members.add(request.user)
        # chat.members.add(user)
        # chat.save()
        # message = Message(sender=user, text=('Привет тест'+str(i)), chat=chat)
        # message.save()
