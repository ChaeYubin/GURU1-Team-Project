from django.contrib import admin
from .models import User, Post, Comment, Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
