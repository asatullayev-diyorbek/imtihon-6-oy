from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category']


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.News, NewsAdmin)
