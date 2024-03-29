from django.db import models
from django.contrib.auth.models import AbstractUser
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


class User(AbstractUser):
    nickname = models.CharField(max_length=20)


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/category/{}/'.format(self.slug)

    class Meta:
        verbose_name_plural = 'categories'


class Tag(models.Model):
    objects = None
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/tag/{}/'.format(self.slug)


class Post(models.Model):
    objects = None
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    head_image = models.ImageField(upload_to='blog/%y/%m/%d/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return '{} :: {}'.format(self.title, self.author)

    def get_absolute_url(self):
        return '/blog/{}/'.format(self.pk)

    def get_update_url(self):
        return self.get_absolute_url() + 'update/'

    def get_create_url(self):
        return self.get_absolute_url() + 'create/'

    def get_delete_url(self):
        return '/blog/delete_post/{}/'.format(self.pk)

    def get_markdown_content(self):
        return markdown(self.content)


class Question(models.Model):
    objects = None
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{} :: {}'.format(self.title, self.author)

    def get_absolute_url(self):
        return '/blog/QnA/{}/'.format(self.pk)

    def get_update_url(self):
        return self.get_absolute_url() + 'update/'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{}'.format(self.pk)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.question.get_absolute_url() + '#comment-id-{}'.format(self.pk)

