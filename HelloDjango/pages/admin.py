from django.contrib import admin
from .models import Post
from .models import CategoryPost
from .models import Quotes
from .models import Links, FriendLinks
from .models import Choice, Question
from .models import Event
from .models import EventCategory
from .models import Gallery
from .models import Books
from .models import CategoryBooks
from .models import News
from .models import CategoryGallery
from .models import Persons
from .models import LogoImage
from .models import ListIcons
from .models import BackgroundImage
from .models import Dictionary
from .models import Suvorov


admin.site.site_header = "Админка сайта PSY-WINGS! - Добро пожаловать в админку!"
admin.site.site_title = "Админка сайта PSY-WINGS!"
admin.site.index_title = "Разделы администрирования"


class ListIconsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_per_page = 20


class SuvorovAdmin(admin.ModelAdmin):
    list_display = 'title',
    search_fields = 'title',


class LogoImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_editable = ('is_published',)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_per_page = 20


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 20


class CategoryBookAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 20


class CategoryGalleryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 20


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 20

    def formatted_hit_count(self, obj):
        return obj.current_hit_count if obj.current_hit_count > 0 else '-'

    formatted_hit_count.admin_order_field = 'hit_count'
    formatted_hit_count.short_description = 'Hits'


class LinksAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title', 'url',)
    search_fields = ('title', 'url',)
    list_per_page = 20


class QuotesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('title',)
    list_per_page = 20


class FriendLinksAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title', 'url',)
    search_fields = ('title', 'url',)
    list_per_page = 20


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_category', 'is_published')
    list_display_links = ('title',)
    search_fields = ('title', 'event_category')
    list_editable = ('is_published',)
    list_per_page = 20


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_per_page = 20


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_per_page = 20

    def formatted_hit_count(self, obj):
        return obj.current_hit_count if obj.current_hit_count > 0 else '-'

    formatted_hit_count.admin_order_field = 'hit_count'
    formatted_hit_count.short_description = 'Hits'


class BooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_per_page = 20


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_per_page = 20


class PersonsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published')
    search_fields = ('title',)
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_per_page = 20


class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('alpha_position',)
    search_fields = ('title',)
    list_per_page = 20


admin.site.register(BackgroundImage)
admin.site.register(ListIcons, ListIconsAdmin)
admin.site.register(LogoImage, LogoImageAdmin)
admin.site.register(CategoryGallery, CategoryGalleryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Persons, PersonsAdmin)
admin.site.register(Books, BooksAdmin)
admin.site.register(CategoryBooks, CategoryBookAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(CategoryPost, CategoryAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(FriendLinks, FriendLinksAdmin)
admin.site.register(Quotes, QuotesAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(Suvorov, SuvorovAdmin)
