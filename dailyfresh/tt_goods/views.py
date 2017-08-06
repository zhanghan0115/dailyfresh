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
    return render(request, 'tt_goods/index.html/', context)



def goods_list(request, type_id, page_index,order_by):
    type_list = TypeInfo.objects.get(pk=type_id)
    orderbystr = '-id' #默认id排
    if order_by =='1':
        orderbystr ='-id'
    elif order_by =='2':
        orderbystr ='gprice'
    elif order_by == '3':
        orderbystr = '-gclick'
    goodslist = type_list.goodsinfo_set.order_by(orderbystr)
    click_list = type_list.goodsinfo_set.order_by('-gclick')[0:2]
    paginator = Paginator(goodslist, 10)  # 创建分页
    page_index = int(page_index)  # 参数page_index是字符串需要转换类型
    if page_index <= 0:
        page_index = 1
    if page_index >= paginator.num_pages:
        page_index = paginator.num_pages  # 判断用户输入是否正确

    page = paginator.page(int(page_index))




    plist = paginator.page_range  # 页码列表
    if paginator.num_pages > 5:
        if page_index <= 2:
            plist = range(1, 6)
        elif page_index >= page.num_pages - 1:
            plist = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            plist = range(page_index - 2, page_index + 3)

    context = {'title': '列表页', 'cart': '1', 'type': type_list, 'goodslist': goodslist, 'clicklist': click_list,
               'page': page, 'pindex_list': plist,'order_by':order_by}
    return render(request, 'tt_goods/list.html', context)




def detail(request,gid):
    try:
        goods = GoodsInfo.objects.get(pk=gid)
        goods.gclick+=1
        goods.save()
        clicklist = goods.gtype.goodsinfo_set.order_by('-gclick')[0:2]
        context = {'title':'详细页','goods':goods,'clicklist':clicklist}
        return render(request,'tt_goods/detail.html',context)
    except:
        return render(request, '404.html')



from haystack.generic_views import SearchView

class MySearchView(SearchView):

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)

        context['title']='搜索结果'
        context['cart'] = '1'
        context['isleft'] = '0'

        return context



