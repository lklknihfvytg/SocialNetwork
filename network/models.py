from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from django.db import models


class Profile(models.Model):
    STATUS_NEW = '0_new'
    STATUS_ACTIVATED = '1_activated'
    STATUS_BANNED = '2_banned'
    STATUS_DELETED = '3_deleted'
    STATUS_CHOICES = [(STATUS_NEW, 'new'), (STATUS_ACTIVATED, 'activated'), (STATUS_BANNED, 'banned'),
                      (STATUS_DELETED, 'deleted')]

    user = models.OneToOneField(User, related_name='profile', verbose_name='User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=45)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_NEW)
    city = models.CharField(max_length=128, blank=True)
    family_status = models.CharField(max_length=45, blank=True)  # !!! доделать !!!
    about = models.CharField(max_length=128, blank=True)
    dark_theme = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='avatar', default='avatar/default.jpg')
    friends = models.ManyToManyField('Profile', related_name='user_friends', blank=True)
    groups = models.ManyToManyField('Group', related_name='user_groups', blank=True)

    def __str__(self):
        return f'{self.user.username} ___ {self.name} {self.surname}'


@receiver(pre_save, sender=Profile)
def name_uppercase(sender, instance, *args, **kwargs):
    instance.name = instance.name.title()
    instance.surname = instance.surname.title()
    instance.city = instance.city.title()


class Group(models.Model):
    STATUS_NEW = '0_new'
    STATUS_ACTIVATED = '1_activated'
    STATUS_BANNED = '2_banned'
    STATUS_DELETED = '3_deleted'
    STATUS_CHOICES = [(STATUS_NEW, 'new'), (STATUS_ACTIVATED, 'activated'), (STATUS_BANNED, 'banned'),
                      (STATUS_DELETED, 'deleted')]

    admin = models.OneToOneField(User, related_name='group_admin', verbose_name='admin', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=45)
    about = models.CharField(max_length=128, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='avatar', default='avatar/default.jpg')

    def __str__(self):
        return self.name


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=800, blank=True)
    image = models.ImageField(upload_to='photos')
    creation_time = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.title


# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()


# ////// Примеры использования
#
# users = User.objects.all().select_related('Profile')
#
# <h2>{{ user.get_full_name }}</h2>
# <ul>
#   <li>Username: {{ user.username }}</li>
#   <li>Location: {{ user.profile.location }}</li>
#   <li>Birth Date: {{ user.profile.birth_date }}</li>
# </ul>
#
# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#     user.save()
