from django.shortcuts import render, redirect
from posts.models import Post, PostLike


def post_by_id(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    return render(request, 'profile_posts.html', {'user': request.user})


def post_like(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    print(request.GET)
    try:
        redirect_to = request.GET.get('next', '')
        post_id = request.GET.get('post_id', '')
        post = Post.objects.get(id=post_id)
        try:
            like = PostLike.objects.get(user_like=request.user, post_like=post)
            like.delete()
        except Exception:
            like = PostLike(user_like=request.user, post_like=post)
            like.save()
    except Exception:
        redirect_to = 'network:feed'

    return redirect(redirect_to)
