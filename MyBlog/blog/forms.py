from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article                 # 指明数据模型来源
        fields = ('title', 'body', 'tags', 'avatar')      # 定义表单包含的字段
