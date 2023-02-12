from django.db import models
from ckeditor.fields import RichTextField


class PageInfo(models.Model):
    title = models.CharField(max_length=225, verbose_name='Название')
    url_tag = models.CharField(max_length=250, verbose_name='URL Tag')
    text = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Landing Page'
        verbose_name_plural = 'Landing Page'
        ordering = ['created_at']
