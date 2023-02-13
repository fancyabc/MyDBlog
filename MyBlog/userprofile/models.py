from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save  # # 引入内置信号

from django.dispatch import receiver


class Profile(models.Model):
    """对Django提供的User进行扩展"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # 与 User 模型构成一对一的关系
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)  # 少量图片可以上传到服务器，大量的可以选择文件服务
    bio = models.TextField(max_length=500, blank=True)      # 个人简介

    def __str__(self):
        return 'user {}'.format(self.user.username)


# 每个`Profile`模型对应唯一的一个`User`模型，形成了对User的外接扩展，因此你可以在`Profile`添加任何想要的字段。
# 这种方法的好处是不需要对`User`进行任何改动，从而拥有完全自定义的数据表

# 信号接收函数，每当新建 User 实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 信号接收函数，每当更新 User 实例时自动调用
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
