from django.contrib import admin
from .models import User, Post, Comment, Category, Tag, Question, Answer


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag, TagAdmin)
