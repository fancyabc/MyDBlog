from django.shortcuts import render
import markdown

# 导入数据模型ArticlePost
from .models import Article


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
