from django.contrib import admin
from .models import PageInfo


class PageInfoAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 20


admin.site.register(PageInfo, PageInfoAdmin)
