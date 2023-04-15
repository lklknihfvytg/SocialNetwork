from django.contrib import admin
from .models import Profile, Zavod, Car


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_time', 'id']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Zavod)
admin.site.register(Car)
