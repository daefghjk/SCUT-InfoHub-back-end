from django.db import models

class User(models.Model):
    openid = models.CharField(primary_key=True, max_length=50)
    session_key = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)
    major = models.CharField(max_length=50)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name

class Post(models.Model):
    post_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=False, blank=False)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return f'Comment by openid:{self.author.openid} on post_id:{self.post.post_id}'

class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='Like'
        
    def __str__(self):
        return f'Comment by openid:{self.author.openid}'
    
