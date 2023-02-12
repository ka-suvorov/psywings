from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    nickname = models.CharField(max_length=250, unique=True, verbose_name='Уникальный псевдоним')
    website = models.URLField(max_length=200, blank=True)
    email = models.EmailField(max_length=220, blank=True, unique=True)
    photo = models.ImageField(upload_to='media/users/pictures', blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
