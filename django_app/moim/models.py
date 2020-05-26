from django.contrib.auth import get_user_model
from django.db import models

from django.utils import timezone

User = get_user_model()


class TimeModel(models.Model):
    created_time = models.DateTimeField(default=timezone.now, null=False)
    update_time = models.DateTimeField(auto_now=True, null=False)
    delete_time = models.DateTimeField(null=True)

    class Meta:
        abstract = True


# 모임 마스터 테이블
class PostMaster(TimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    like_users = models.ManyToManyField(User, related_name="like_post")

    def add_comment(self, user, content):
        return self.comment_set.create(user=user, content=content)


# 모임 댓글 테이블
class Comment(TimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(PostMaster, on_delete=models.CASCADE)
