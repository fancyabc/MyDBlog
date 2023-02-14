
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Article


class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    context_object_name = 'notices'
    template_name = 'notice/list.html'
    login_url = '/userprofile/login/'

    def get_queryset(self):
        """ 未读通知的查询集"""
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
    """更新通知状态"""

    def get(self, request):
        notice_id = request.GET.get('notice_id')
        if notice_id:
            article = Article.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')