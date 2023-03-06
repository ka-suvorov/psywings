from django import template
from ..models import Quotes
from ..models import CategoryPost
from ..models import CategoryBooks
from ..models import FriendLinks
from ..models import Gallery
from ..models import Event
from ..models import EventCategory
from ..models import CategoryGallery
from ..models import News
from ..models import LogoImage
from ..models import BackgroundImage
from ..models import ListIcons
from ..models import Post
from ..models import Books
from ..models import Dictionary
from ..models import Persons
from ..models import Question


register = template.Library()


@register.simple_tag(name='background_image_url')
def background_image_url():
    """ """
    return BackgroundImage.objects.get().img.url


@register.simple_tag(name='get_image_logo')
def get_logo():
    return LogoImage.objects.all()[0:1]


@register.simple_tag(name='get_friends_list')
def get_friends_list():
    return FriendLinks.objects.all().order_by("title")


@register.simple_tag(name='get_post_categories')
def get_post_categories():
    return CategoryPost.objects.all().order_by('updated_at')


@register.simple_tag(name='get_book_categories')
def get_book_categories():
    return CategoryBooks.objects.all().order_by('updated_at')


@register.simple_tag(name='get_list_quotes')
def get_quotes():
    return Quotes.objects.all().order_by('?').filter(is_published=True)[0:1]


@register.simple_tag(name='get_list_gallery')
def get_list_gallery():
    return Gallery.objects.all().order_by('?').filter(is_published=True)[0:1]


@register.simple_tag(name='get_events_list')
def get_events():
    return Event.objects.all()


@register.simple_tag(name='get_event_category_list')
def get_event_category():
    return EventCategory.objects.all()


@register.simple_tag(name='get_fresh_news')
def get_fresh_news():
    return News.objects.all().order_by('-created_at').filter(is_published=True)[0:3]


@register.simple_tag(name='get_gallery_categories')
def get_post_categories():
    return CategoryGallery.objects.all()


@register.simple_tag(name='get_list_icons')
def get_icons():
    return ListIcons.objects.all().order_by('date')


@register.simple_tag(name='get_stat_posts')
def get_stat_posts():
    return Post.objects.count()


@register.simple_tag(name='get_stat_gallery')
def get_stat_gallery():
    return Gallery.objects.count()


@register.simple_tag(name='get_stat_books')
def get_stat_books():
    return Books.objects.count()


@register.simple_tag(name='get_stat_terms')
def get_stat_terms():
    return Dictionary.objects.count()


@register.simple_tag(name='get_stat_polls')
def get_stat_polls():
    return Question.objects.count()


@register.simple_tag(name='get_stat_persons')
def get_stat_terms():
    return Persons.objects.count()


@register.simple_tag(name='get_stat_friends')
def get_stat_friends():
    return FriendLinks.objects.count()


@register.filter()
def class_name(value):
    return value.__class__.__name__
