from django import template
from ..models import Quotas
from ..models import CategoryPost
from ..models import CategoryBooks
from ..models import FriendLinks
from ..models import Gallery
from ..models import Event
from ..models import EventCategory
from ..models import CategoryGallery
from ..models import News

register = template.Library()


@register.simple_tag(name='get_friends_list')
def get_friends_list():
    return FriendLinks.objects.order_by("title")


@register.simple_tag(name='get_post_categories')
def get_post_categories():
    return CategoryPost.objects.all()


@register.simple_tag(name='get_book_categories')
def get_book_categories():
    return CategoryBooks.objects.all()


@register.simple_tag(name='get_list_quotas')
def get_quotes():
    return Quotas.objects.all().order_by('?').filter(is_published=True)[0:1]


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


@register.filter()
def class_name(value):
    return value.__class__.__name__


@register.simple_tag(name='get_gallery_categories')
def get_post_categories():
    return CategoryGallery.objects.all()
