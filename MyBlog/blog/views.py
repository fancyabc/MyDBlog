from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

import markdown


from .models import Article, ArticleColumn
from .forms import ArticleForm
from comment.models import Comment


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    article_list = Article.objects.all()

    if search is not None:
        article_list = Article.objects.filter(
            Q(title__icontains=search) |
            Q(body__contains=search)
        ).order_by('-view_counts')
    else:
        search = ''

    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    if order == 'view_counts':
        # 按热度排序博文
        article_list = article_list.order_by('-view_counts')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {'articles': articles,
               'order': order,
               'search': search,
               'column': column,
               'tag': tag,
               }

    return render(request, 'blog/list.html', context)


def article_detail(request, id):
    # 取出相应的文章
    article = Article.objects.get(id=id)
    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    article.view_counts += 1
    article.save(update_fields=['view_counts'])  # `update_fields=[]`指定了数据库只更新`total_views`字段，优化执行效率。
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)

    context = {'article': article, 'toc': md.toc, 'comments': comments}
    # 载入模板，并返回context对象
    return render(request, 'blog/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        article_post_form = ArticleForm(data=request.POST)

        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)   # 指定目前登录的用户为作者
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()

            article_post_form.save_m2m()    # 保存 tags 的多对多关系
            return redirect("blog:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticleForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'blog/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect("blog:article_list")


# 安全删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = Article.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":

        article_post_form = ArticleForm(data=request.POST)

        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()

            return redirect("blog:article_detail", id=id)

        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        article_post_form = ArticleForm()
        columns = ArticleColumn.objects.all()

        context = {'article': article,
                   'article_post_form': article_post_form,
                   'columns': columns
                   }
        # 将响应返回到模板中
        return render(request, 'blog/update.html', context)
