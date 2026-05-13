from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Store the country name to fetch data from restcountries.com API
    country = models.CharField(max_length=100, default='India', help_text="Enter a country name (e.g. France, Japan)")
    
    # Store the URL of the AI-generated cover image
    cover_image_url = models.URLField(max_length=1024, blank=True, null=True)
    
    # Likes
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    
    # Store the sentiment determined by the Hugging Face AI API
    SENTIMENT_CHOICES = [
        ('Positive', 'Positive 😊'),
        ('Neutral', 'Neutral 😐'),
        ('Negative', 'Negative 😠'),
    ]
    sentiment_label = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} on {self.post.title}'
