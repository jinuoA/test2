# -*- coding:utf-8 -*-
from django.shortcuts import render,Http404,HttpResponseRedirect
from xphone.models import *
from blog.models import *
import logging
from django.http import HttpResponse
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import json
import qiniu.conf
import qiniu.rs
import qiniu.io

# Create your views here.

BUCKET_NAME = "1107194939@qq.com"
qiniu.conf.ACCESS_KEY = "flTet2awAnDzYTQh2RePRJe07lzmFpIvP5GZwaSx"
qiniu.conf.SECRET_KEY = "_3qrfvrvttMpBrFKOG1NbxarDZBCJS6YAPdacTxi"


logger = logging.getLogger('blog.views')

# 分页代码
def getPage(request, article_list):
    paginator = Paginator(article_list, 5)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list



def blog(request):
    try:

        #文章内容
        article_list = Article.objects.all()
        hot_articles = Article.objects.order_by("-click_count").all()[:4]
    except Exception as e:
        logger.error(e)

    return render(request,'blog.html',locals())



def blog_video(request):
    try:
        video_list = Video.objects.order_by()
    except Exception as e:
        logger.error(e)

    return render(request,'blog_video.html',locals())


def video(request,id):
    try:
        video_list = Video.objects.filter(id=id)

    except:
        pass
    return render(request,'demo.html',locals())


def blog_picture(request):
    try:
        proPic_list = ProPic.objects.order_by("id")

    except Exception as e:
        logger.error(e)

    return render(request,'blog_picture.html',locals())


# 手机图片详细页面
def picture_details(request, id):
    # 图片详情2
    picture2_list = Picture2.objects.filter(ProPic_id=id)
    picture_imgs = Picture_details.objects.filter(ProPic_id=id)

    return render(request, 'picture-details.html', locals())



def blog_news(request):
    try:
        # 文章内容
        article_list = Article.objects.all()
    except Exception as e:
        logger.error(e)

    return render(request,'blog_news.html',locals())


def article_details(request,id):
    try:
        article = Article.objects.filter(id=id).all()[0]
        # print article
        hot_articles = Article.objects.order_by("-click_count").all()[:4]
        count = Article.objects.count()
        # 文章浏览量
        see_time = Article.objects.filter(id=id)[0].click_count + 1
        # print see_time
        Article.objects.filter(id=id).update(click_count=see_time)
        # 博客评论
        comments = Comment.objects.filter(article_id=id)
        # print blog_comments
        # 评论统计
        all_comments = Comment.objects.count()
        my_comments = Comment.objects.filter(user=request.user.id).count()
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse("页面不存在")
    except Exception as e:
        pass
    return render(request,'article_details.html',locals())


#qiniu
def qiniu_video(request):
    return render(request, 'qiniu_video.html',locals())

def uptoken(request):
    policy = qiniu.rs.PutPolicy(BUCKET_NAME)
    token = policy.token()
    data = {'uptoken': token}
    return HttpResponse(json.dumps(data), content_type="application/json")


#分页代码

def getPage(request,article_list):
    paginator = Paginator(article_list, 3)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

#收藏次数
@csrf_exempt
def collection_time(request):
    try:
        if request.method == 'POST':
            ids = request.POST
            for id in ids:
                per_id = ids[id]
                collect = Article.objects.filter(id=int(per_id))[0].collect_count+1
                Article.objects.filter(id=int(per_id)).update(collect_count=collect)
    except Exception as e:
        logger.error(e)


# 发表评论
def comment_post(request, id):
    try:
        if request.user.is_authenticated():
            if request.method == 'POST':
                talk = request.POST.get('text')
                # print id
                # print talk
                # print request.user.id
                comment = Comment.objects.create(user_id=request.user.id,
                                                 username=request.user.username,
                                                 # user_img=request.user.avatar,
                                                 content=talk,
                                                 article_id=id)
                comment.save()
            else:
                return HttpResponse('评论失败')
        else:
            return HttpResponseRedirect('/login')
    except Exception as e:
        logger.error(e)
    return HttpResponseRedirect('/article_details/%s' % id)

# 博客文章查询
def blog_search(request):
    try:
        # print 'aaaaa'
        hot_articles = Article.objects.order_by("-click_count").all()[:4]
        if request.method == 'POST':
            search_title = request.POST.get("blog_search")
            # print search_title
            article_list = getPage(request, Article.objects.filter(title__icontains=search_title).all())
            # print article_list
            return render(request, 'blog.html', locals())
        else:
            return render(request, 'blog.html', locals())
    except Exception as e:
        logger.error(e)