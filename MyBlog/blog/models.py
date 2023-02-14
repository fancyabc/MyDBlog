from django.db import models

# 导入内建的User模型。
from django.contrib.auth.models import User

from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager
from PIL import Image


class ArticleColumn(models.Model):
    """栏目的 Model"""

    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Article(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    view_counts = models.PositiveIntegerField(default=0)
    tags = TaggableManager(blank=True)
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)  # 文章标题图
    likes = models.PositiveIntegerField(default=0)

    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )   # 文章栏目的 “一对多” 外键

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)   # ordering 指定模型返回的数据的排列顺序,'-created' 表明数据应该以倒序排列

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.id])

    def save(self, *args, **kwargs):
        article = super(Article, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article
