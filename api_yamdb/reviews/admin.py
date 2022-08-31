from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'author', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'category', 'description')
    empty_value_display = '-пусто-'


@admin.register(models.GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre')
    empty_value_display = '-пусто-'


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'role', 'bio', 'first_name', 'last_name')
    list_filter = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'
