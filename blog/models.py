from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistices.models import ReadNumExpandMethod


class Category(models.Model):
    """博文分类"""
    name = models.CharField('分类名称', max_length=20)
    slug = models.SlugField('URL缩写', max_length=50)
    description = models.TextField('备注', max_length=200, null=True)

    def __str__(self):
        return self.name


class ArticlePublicManager(models.Manager):
    """
    博客日志管理器
    过滤状态为发布的文章
    """
    def get_queryset(self):
        return super(ArticlePublicManager, self).get_queryset().filter(status='public')


class Article(models.Model, ReadNumExpandMethod):
    """博客文章"""
    STATUS_CHOICE = (
        ('Private', '私密'),
        ('public', '发布'),
    )
    title = models.CharField('标题', max_length=50)
    slug = models.SlugField('URL缩写', max_length=100, unique=True)
    author = models.ForeignKey(User, related_name='blog_article', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, related_name='blog_article')
    image = models.ImageField('博文主图', null=True, blank=True, upload_to="ArticlePictures/")
    body = RichTextUploadingField('正文')
    tags = TaggableManager()
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)
    status = models.CharField('发布状态', max_length=10, choices=STATUS_CHOICE, default='Private')

    object = models.Manager()
    # 发布状态为 发布的文章
    Public_objects = ArticlePublicManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


