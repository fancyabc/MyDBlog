from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

import markdown

# 导入数据模型ArticlePost
from .models import Article
from .forms import ArticleForm


def article_list(request):
    # 取出所有博客文章
    articles = Article.objects.all()
    # 需要传递给模板（templates）的对象
    context = {'articles': articles }
    # render函数：载入模板，并返回context对象
    return render(request, 'blog/list.html', context)


def article_detail(request, id):
    # 取出相应的文章
    article = Article.objects.get(id=id)
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    context = {'article': article}
    # 载入模板，并返回context对象
    return render(request, 'blog/detail.html', context)


def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticleForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("blog:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticleForm()
        # 赋值上下文
        context = { 'article_post_form': article_post_form }
        # 返回模板
        return render(request, 'blog/create.html', context)


def article_delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect("blog:article_list")


# 安全删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")
