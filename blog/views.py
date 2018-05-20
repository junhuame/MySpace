from django.shortcuts import render, get_object_or_404, render_to_response
from django.db.models import Count
from django.conf import settings
from django.core.paginator import Paginator

from .models import Article, Category
from taggit.models import Tag
from read_statistices.utils import read_statics_once_read
from MySpace.utils import get_blog_paginator, get_blog_paginator_plus


def blog_list(request):
    """
    博客列表页
    """
    articles_list = Article.Public_objects.all()
    paginator = Paginator(articles_list, settings.EACH_PAGE_ARTICLE_NUMBER)

    articles = get_blog_paginator(request, paginator)
    page_range = get_blog_paginator_plus(request, articles, paginator)

    return render(request, 'blog/index.html', {'articles': articles, 'page_range': page_range})


def blog_category_list(request, slug):
    """博客分类列表"""
    category = get_object_or_404(Category, slug=slug)
    category_articles = Article.Public_objects.filter(category=category)
    paginator = Paginator(category_articles, settings.EACH_PAGE_ARTICLE_NUMBER)

    articles = get_blog_paginator(request, paginator)
    page_range = get_blog_paginator_plus(request, articles, paginator)

    return render(request, 'blog/blog-category.html', {'articles': articles,
                                                       'page_range': page_range,
                                                       'category': category})


def blog_tag_list(request, slug):
    """博客标签"""
    tags = get_object_or_404(Tag, slug=slug)
    tag_articles = Article.Public_objects.filter(tags__slug=tags)
    paginator = Paginator(tag_articles, settings.EACH_PAGE_ARTICLE_NUMBER)
    articles = get_blog_paginator(request, paginator)
    page_range = get_blog_paginator_plus(request, articles, paginator)

    return render(request, 'blog/blog-tags.html', {'articles': articles,
                                                    'page_range': page_range,
                                                    'tags': tags})



def base(request):
    return render(request, 'base.html')


def blog_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    read_cookie_key = read_statics_once_read(request, article)
    # 利用标签，获取相关日志
    article_tags_ids = article.tags.values_list('id', flat=True)
    similar_articles = Article.Public_objects.filter(tags__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]
    # 实现上一页与下一页
    previous_article = Article.Public_objects.filter(created__gt=article.created).last()
    next_article = Article.Public_objects.filter(created__lt=article.created).first()

    response = render_to_response( 'blog/detail.html', {'article': article,
                                                        'similar_articles': similar_articles,
                                                        'previous_article': previous_article,
                                                        'next_article': next_article})
    response.set_cookie(read_cookie_key, 'true') # 阅读cookie标记
    return response


def blog_archive(request):
    """
    博客归档
    """
    articles = Article.Public_objects.all()
    return render(request, 'blog/blog-archive.html', {'articles': articles})


def about(request):
    return render(request, 'about.html')