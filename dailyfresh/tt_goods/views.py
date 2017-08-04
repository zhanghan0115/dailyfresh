# coding=utf-8
from django.shortcuts import render
from models import TypeInfo, GoodsInfo
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    '''需要输出的分类信息：分类信息，最新的4个商品，人气最高的3个商品，种类6种所以6组信息'''
    type_list = TypeInfo.objects.all()
    list = []
    for typeinfo in type_list:
        list.append({'type': typeinfo, 'list_new': typeinfo.goodsinfo_set.order_by('-id')[0:4],
                     'list_click': typeinfo.goodsinfo_set.order_by('-gclick')[0:3]})
    context = {'title': '首页', 'cart': '1', 'list': list}
    return render(request, 'tt_goods/index.html/',context)
    # type_list = TypeInfo.objects.all()
    # list = []
    # for typeinfo in type_list:
    #     list.append({
    #         'type': typeinfo,
    #         'list_new': typeinfo.goodsinfo_set.order_by('-id')[0:4],
    #         'list_click': typeinfo.goodsinfo_set.order_by('-gclick')[0:3]
    #     })
    # context = {'title': '首页', 'cart': '1', 'list': list}
    # return render(request, 'tt_goods/index.html', context)


def goods_list(request,type_id,page_index):
    type_list = TypeInfo.objects.get(pk=type_id)
    goodslist = type_list.goodsinfo_set.order_by('-id')
    click_list = type_list.goodsinfo_set.order_by('-gclick')[0:2]
    p = Paginator(goodslist,10) #创建分页
    page_index = int(page_index) #参数page_index是字符串需要转换类型
    if page_index <= 0:
        page_index = 1
    if page_index >= p.num_pages:
        page_index = p.num_pages  #判断用户输入是否正确

    page = p.page(int(page_index))

    plist = p.page_range#页码列表
    if p.num_pages > 5:
        if page_index <= 2:
            plist = range(1, 6)
        elif page_index >= p.num_pages - 1:
            plist = range(p.num_pages - 4, p.num_pages + 1)
        else:
            plist = range(page_index - 2, page_index + 3)




    context = {'title':'列表页','cart':'1','type':type_list,'goodslist':goodslist,'clicklist':click_list,'page':page,'pageindex':plist}
    return render(request,'tt_goods/list.html',context)