from django.contrib import admin
from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """博文分类管理"""
    list_display = ('name', 'slug', 'description')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """博客文章管理"""
    list_display = ('title', 'slug', 'category', 'status', 'get_read_num', 'created')
    list_editable = ('status',)
    search_fields = ('title', 'body')
    date_hierarchy = 'created'
    list_filter = ('category', 'status', 'created')
    list_per_page = 20


# 自定义管理站点的名称和URL标题
admin.site.site_header = '网站管理'
admin.site.site_title = '博客后台管理'


