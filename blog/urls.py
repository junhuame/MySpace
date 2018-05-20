from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', view=views.blog_list, name='blog_list'),
    url(r'^base/$', view=views.base, name='base'),
    url(r'^article/(?P<slug>[\w-]+)/$', view=views.blog_detail, name='blog_detail'),
    url(r'^category/(?P<slug>[\w-]+)/$', view=views.blog_category_list, name='blog_category_list'),
    url(r'^tag/(?P<slug>[\w-]+)/$', view=views.blog_tag_list, name='blog_tag_list'),
    url(r'^archive/$', view=views.blog_archive, name='blog_archive'),
    url(r'^about/$', view=views.about, name='about'),

]
