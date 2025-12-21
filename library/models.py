from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.email if self.user else "Author (no user)"

    
  

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='books/')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)



def __str__(self):
    return self.title

