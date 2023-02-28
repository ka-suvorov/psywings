from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q
from django.contrib.auth.models import User
from cffi.backend_ctypes import xrange
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
import datetime
from django.utils import timezone
from hitcount.models import HitCountMixin, HitCount


# Models for Post section
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
    title = models.CharField(max_length=250, verbose_name='Заголовок Статьи', unique=True)
    text = RichTextUploadingField()
    foto = models.ImageField(upload_to='media/pic/%Y/%m/%d/', verbose_name='Картинка', blank=True, null=True)
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
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-is_published']


# Function and model for Alphabet dictionary
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


class Dictionary(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False, verbose_name=_('The Term'),
                             help_text=_('The Term being described'))
    text = models.TextField(blank=False, verbose_name=_('The Explanation'),
                            help_text=_('The description of the term being explained'))
    alpha_position = models.CharField(max_length=2, db_index=True, editable=True, blank=False, null=False,
                                      choices=ALPHABET_CHOICES, verbose_name=_('Позиция в алфавите'),
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


# Model for quotes section
class Quotes(models.Model):
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
        ordering = ['name']


# Models for poll sections
class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Вопрос")
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


# Models for links section
class LinksManager(models.Manager):

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Links(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, blank=False, null=False, verbose_name='Название сайта')
    url = models.URLField(verbose_name='URL Сайта')
    content = RichTextUploadingField(blank=True)
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


class FriendLinks(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, blank=False, null=False, verbose_name='Название сайта')
    url = models.URLField(verbose_name='URL Сайта')
    content = RichTextUploadingField(blank=True)
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


# model for News section
class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=250, verbose_name='Заголовок новости')
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-updated_at']


# Models for Book sections
class CategoryBookManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


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
    book = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField()
    objects = BooksManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']


# Models for Event section
class EventManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(title__icontains=query) | Q(foto__icontains=query) | Q(text__icontains=query))
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
    foto = models.ImageField(upload_to='media/event/%Y/%m/%d/', verbose_name='Картинка', blank=True, null=True)
    text = RichTextUploadingField()
    event_date = models.DateTimeField(verbose_name='Дата события', null=True, blank=True)
    event_category = models.ForeignKey(EventCategory, on_delete=models.PROTECT, blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    objects = EventManager()

    def get_search_url(self):
        return reverse_lazy('Event_detail', args=[self.pk])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Памятная дата'
        verbose_name_plural = 'Памятные даты'
        ordering = ['title']


# Models for gallery section
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


class PersonsManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(text__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Persons(models.Model):
    title = models.CharField(max_length=250, verbose_name='Персоналия')
    foto = models.ImageField(upload_to='media/event/%Y/%m/%d/', verbose_name='Картинка', blank=True, null=True)
    text = RichTextUploadingField()
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    objects = PersonsManager()

    def get_search_url(self):
        return reverse_lazy('person_detail', args=[self.pk])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Персоналия'
        verbose_name_plural = 'Персоналии'
        ordering = ['title']


class LogoImage(models.Model):
    title = models.CharField(max_length=250, verbose_name='Логотип')
    foto = models.ImageField(upload_to='media/logo/%Y/%m/%d/', verbose_name='LOGO', blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Логотип'
        verbose_name_plural = 'Логотипы'
        ordering = ['title']
        

class ListIcons(models.Model):
    title = models.CharField(max_length=250, verbose_name='Иконки в лендинг')
    foto = models.ImageField(upload_to='media/index/%Y/%m/%d/', verbose_name='IMG_index', blank=True, null=True)
    inside_url = models.CharField(max_length=250)
    date = models.DateTimeField()
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Иконка в лендинг'
        verbose_name_plural = 'Иконки в лендинг'
        ordering = ['title']


class SingletonModel(models.Model):
    """Singleton Django Model

    Ensures there's always only one entry in the database, and can fix the
    table (by deleting extra entries) even if added via another mechanism.

    Also has a static load() method which always returns the object - from
    the database if possible, or a new empty (default) instance if the
    database is still empty. If your instance has sane defaults (recommended),
    you can use it immediately without worrying if it was saved to the
    database or not.

    Useful for things like system-wide user-editable settings.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class BackgroundImage(SingletonModel):
    img = models.ImageField(upload_to='background-image')
