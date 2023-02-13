from django.contrib import admin

# Register your models here.
from .models import Article

# 注册Article 到admin中
admin.site.register(Article)
