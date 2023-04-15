from django.contrib import admin
from .models import Post, PostLike, PostComment, RePost


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_time', 'id']


class PostLikeAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_time']


class PostCommentAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_time']


class RePostAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_time']


admin.site.register(Post, PostAdmin)
admin.site.register(RePost, RePostAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(PostComment, PostCommentAdmin)
