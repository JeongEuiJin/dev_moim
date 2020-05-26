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


class PostMaster(TimeModel):
    """
    모임 마스터 테이블
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    like_users = models.ManyToManyField(User, related_name="like_posts", through='PostLike')

    def add_comment(self, user, content):
        '''
        댓글 바로 추가
        :param user: 추가하는 유저
        :param content: 댓글 내용
        :return: 생성
        '''
        return self.comment_set.create(user=user, content=content)

    def like_count(self):
        '''
        모임 마스터 테이블의 좋아요 갯수
        :return: 좋아요 갯수
        '''
        return self.postlike_set.count()


class PostLike(TimeModel):
    """
    모임 마스터 좋아요 테이블
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostMaster, on_delete=models.CASCADE)


class Comment(TimeModel):
    """
    모임 댓글 테이블
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(PostMaster, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User, related_name='like_comments', through='CommentLike')


class CommentLike(TimeModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
