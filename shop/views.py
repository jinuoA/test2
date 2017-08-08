# -*- coding:utf-8 -*-
from django.shortcuts import render,Http404
from xphone.models import *
from shop.models import *
import logging
from django.views.decorators.cache import cache_page
# Create your views here.


logger = logging.getLogger('shop.views')


@cache_page(60*15)
def store(request):
    try:
        #商品种类
        tag_list = Navtags.objects.all()
        #搜索
        search_list = Search.objects.all()
        #商品
        good_lsit = ShopSales.objects.all()[:3]
        #配件
        Oneplus_list = ShopSales.objects.all()[4:8]
        rim_list = ShopSales.objects.all()[9:13]
        #购机服务
        service_list = ServerContent.objects.all()
        nav_list = Navtags.objects.all()
    except Exception as e:
        logger.error(e)
    return render(request,'store.html',locals())

def products(request):
    try:
        pass
    except Exception as e:
        logger.error(u"访问的页面不存在")
    return render(request,'products.html',locals())


@cache_page(60*15)
def phone(request,id):
    try:
        nav_list = Navtags.objects.all()

        try:
            good_list = TagGoods.objects.filter(Navtags_id=id)
            ad_list = Ad.objects.filter(Navtags_id=id)
        except:
            pass
    except Exception as e:
        logger.error(e)
    return render(request,'phone.html',locals())


@cache_page(60*15)
def product_details(request,id):
    try:
        sale = ShopSales.objects.all()

        try:
            product = Product_details.objects.filter(sale_id=id)[0:1]
            product_list = Product_details.objects.filter(sale_id=id)[1:5]
            print(product_list)
            #选择颜色
            pro_color = Color.objects.filter(good_id=id)
            arg_list = Arg.objects.filter(sale_id=id)
            pro_list = Product_desc.objects.filter(sale_id=id)[0:1]
            pro_list1 = Product_desc.objects.filter(sale_id=id)[1:2]
            prob_list = Prob.objects.all()
        except Product_details.DoesNotExist:
            raise Http404

    except Exception as e:
        pass
    return render(request, 'product_details.html', locals())
