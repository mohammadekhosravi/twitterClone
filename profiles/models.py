from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/avatars/', default='avatar.png')
    header = models.ImageField(upload_to='users/headers/', default='header.jpg')
    bio = models.CharField(max_length= 240, blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)


    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))
