from django.contrib import admin
from .models import Profile, Photo


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_time', 'id']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Photo)
