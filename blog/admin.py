from django.contrib import admin
from .models import User, Post, Comment, Category


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
