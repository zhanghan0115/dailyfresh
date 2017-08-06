#coding=utf-8
#引入注册对象
from django.template import Library
register=Library()

#使用装饰器进行注册
@register.filter
def page_list(page):
    plist = page.paginator.page_range  # 页码列表
    num_pages= page.paginator.num_pages
    page_index = page.number
    if num_pages > 5:
        if page_index <= 2:
            plist = range(1, 6)
        elif page_index >= num_pages  - 1:
            plist = range(num_pages  - 4,num_pages  + 1)
        else:
            plist = range(page_index - 2, page_index + 3)

    return plist

