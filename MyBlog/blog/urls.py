from django.urls import path
from . import views

# 正在部署的应用的名称
app_name = 'blog'

urlpatterns = [
    path('article-list/', views.article_list, name='article_list'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article_create/', views.article_create, name='article_create'),
    path('article_delete/<int:id>/', views.article_delete, name='article_delete'),
    # 安全删除文章
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    path('article_update/<int:id>/', views.article_update, name='article_update'),

    path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'),
]
