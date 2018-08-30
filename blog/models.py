import markdown
from django.db import models
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
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
    summary = models.CharField('文章摘要', max_length=230, blank=True)
    body = models.TextField('正文')
    tags = TaggableManager()
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('更新时间', auto_now=True)
    status = models.CharField('发布状态', max_length=10, choices=STATUS_CHOICE, default='Private')

    object = models.Manager()
    # 发布状态为 发布的文章
    Public_objects = ArticlePublicManager()

    def __str__(self):
        return self.title

    # 自动生成文章摘要
    def save(self, *args, **kwargs):    
        # 如果没有填写摘要
        if not self.summary:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.summary = strip_tags(md.convert(self.body))[:200]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']


