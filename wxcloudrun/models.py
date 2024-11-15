from django.db import models

class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)
    major = models.CharField(max_length=10)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=False, blank=False)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return f'Comment by uid:{self.author_id} on post_id:{self.post_id}'
