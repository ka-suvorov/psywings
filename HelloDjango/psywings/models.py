from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q
from django.contrib.auth.models import User
from cffi.backend_ctypes import xrange
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
import datetime
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from hitcount.models import HitCountMixin, HitCount


class CategoryPostsManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


# Category model for using in Post and Video


class CategoryPost(models.Model):
    post_category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=225, db_index=True, verbose_name='Название Категория', unique=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    objects = CategoryPostsManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория для поста'
        verbose_name_plural = 'Категории для постов'
        ordering = ['-is_published']


# Class for search in Posts


class PostsManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(text__icontains=query) )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=250, verbose_name='Заголовок новости', unique=True)
    url = models.SlugField(max_length=255, unique=True)
    text = RichTextField()
    views = models.PositiveIntegerField(default=0, blank=True)
    pict = models.ImageField(upload_to='media/pic/%Y/%m/%d/', verbose_name='Картинка', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(CategoryPost, on_delete=models.PROTECT, null=True)
    objects = PostsManager()
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    def current_hit_count(self):
        return self.hit_count.hits

    def get_search_url(self):
        return reverse_lazy('Post_detail', args=[self.pk])

    def __str__(self):
        """Return title and username."""
        return '{} by @{}'.format(self.title, self.user.username)

    def save(self, *args, **kwargs):
        self.url = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-is_published']


# Alphabet Function for range values between alphabet letters


def get_alphabet(begin='а', end='я'):
    # Return a list of Alphabet entries in a configurable range

    dictionary = []
    begin_num = ord(begin)
    end_num = ord(end)
    for number in xrange(begin_num, end_num + 1):
        character = chr(number)
        dictionary.append((character, character))
    return dictionary


# Alphabet Constant for re-use in context and views
ALPHABET_CHOICES = get_alphabet()


# Class for advanced manager dictionary and books models: search and filling alphabet list


class DictionaryManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(text__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs

    def alphabetized_list(self, valid_letters=[]):

        alphabet_list = dict({})
        entries = super(DictionaryManager, self).get_queryset().using('default').filter(is_published=True).order_by(
            'alpha_position', 'title')

        if len(valid_letters) > 0:
            entries = entries.filter(alpha_position__in=valid_letters)

        for e in entries:
            alpha = e.alpha_position
            if alpha in alphabet_list:
                alphabet_list[alpha].append(e)
            else:
                alphabet_list[alpha] = [e]

        return alphabet_list


# Class Dictionary


class Dictionary(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('The Term'),
                             help_text=_('The Term being described'))
    text = models.TextField(blank=False, verbose_name=_('The Explanation'),
                            help_text=_('The description of the term being explained'))
    alpha_position = models.CharField(max_length=2, db_index=True, editable=True, blank=False, null=False,
                                      choices=ALPHABET_CHOICES, verbose_name=_('Alphabet Position'),
                                      help_text=_('Show this entry under which Alphabet position'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    objects = DictionaryManager()

    class Meta:
        verbose_name = 'Запись в словаре'
        verbose_name_plural = 'Все записи в словаре'

    def __unicode__(self):
        return "%s" % self.title


# Class for search in Categories Post and Video


class LinksManager(models.Manager):

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


# Links model


class Links(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, blank=False, null=False, verbose_name='Название сайта')
    url = models.URLField(verbose_name='URL Сайта')
    description = models.TextField(blank=True, null=True, verbose_name='Описание сайта')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    objects = LinksManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сайт - URL'
        verbose_name_plural = 'Сайты - URLs'
        ordering = ['title']


# Quotes model section


class Quotas(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, verbose_name='ФИО Деятеля')
    text = models.TextField(blank=True, null=True, verbose_name='Цитата')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'
        ordering = ['-is_published']


# Polls

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


    # Friends Links
    
class FriendLinks(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, blank=False, null=False, verbose_name='Название сайта')
    url = models.URLField(verbose_name='URL Сайта')
    description = models.TextField(blank=True, null=True, verbose_name='Описание сайта')
    pict = models.ImageField(upload_to='media/pic/%Y/%m/%d/', verbose_name='Картинка', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    objects = LinksManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'URL сайта друзей'
        verbose_name_plural = 'URL сайтов друзей'
        ordering = ['-is_published']


class CategoryBookManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


    # Gallery image section
    
class CategoryGallery(models.Model):
    title = models.CharField(max_length=225, verbose_name='Название категории')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория фотографий'
        verbose_name_plural = 'Категории фотографий'
        ordering = ['title']


class Gallery(models.Model):
    title = models.CharField(max_length=225, verbose_name='Название')
    foto = models.ImageField(upload_to='media/pic/%Y/%m/%d/', verbose_name='Картинка', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    image_category = models.ForeignKey(CategoryGallery, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['created_at']

        
        #Event section

class EventManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(title__icontains=query) | Q(foto__icontains=query))
            qs = qs.filter(or_lookup)

        return qs


class EventCategory(models.Model):
    title = models.CharField(max_length=250, verbose_name='Категория события')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категоря памятной даты'
        verbose_name_plural = 'Категории памятных дат'
        ordering = ['title']


class Event(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок события')
    url = models.SlugField(max_length=255, unique=True)
    foto = models.ImageField(upload_to='media/eventpic/%Y/%m/%d/', verbose_name='Картинка', blank=True, null=True)
    text = RichTextField()
    event_date = models.DateTimeField(verbose_name='Дата события', null=True, blank=True)
    event_category = models.ForeignKey(EventCategory, on_delete=models.PROTECT, blank=True, null=True)
    manager = models.CharField(max_length=60, blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    objects = EventManager()

    def get_search_url(self):
        return reverse_lazy('Event_detail', args=[self.pk])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.url = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Памятная дата'
        verbose_name_plural = 'Памятные даты'
        ordering = ['title']

        
        # Book list section

class CategoryBooks(models.Model):
    book_category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=225, db_index=True, verbose_name='Название Категория', unique=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    objects = CategoryBookManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория для книг'
        verbose_name_plural = 'Категории для книг'
        ordering = ['-is_published']


class BooksManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(book__icontains=query) )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Books(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название книги')
    book = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField()
    objects = BooksManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['book']


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    message = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-updated_at']

