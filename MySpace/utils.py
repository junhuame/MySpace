from django.core.paginator import EmptyPage, PageNotAnInteger


# 利用django提供的分页器进行分页
def get_blog_paginator(request, paginator):
    page = request.GET.get('page')  # 获取url的页面参数（GET请求）
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return articles


# 优化分页效果，增加首页、尾页与分页范围
def get_blog_paginator_plus(request, obj, paginator):
    current_page = obj.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(current_page - 2, 1), current_page)) + \
                 list(range(current_page, min(current_page + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    return page_range