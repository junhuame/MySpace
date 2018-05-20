from django import template
from blog.models import Article, Category
from taggit.models import Tag
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('blog/tags/category-sidebar.html')
def get_all_categories():
    """文章分类"""
    categories = Category.objects.annotate(category_count=Count('blog_article'))

    return {'categories': categories, }


@register.inclusion_tag('blog/tags/tag-cloud.html')
def get_all_tag():
    """标签云"""
    tag_cloud = Tag.objects.all()
    return {'tag_cloud': tag_cloud, }
