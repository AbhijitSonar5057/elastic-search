from email.policy import default
from django.db import models

# Create your models here.



class ElasticDemo(models.Model):
    book_name=models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    price=models.CharField(max_length=70)
    content = models.TextField()
    created_at=models.DateField(auto_now_add=True,)
    