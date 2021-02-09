from django.db import models

# Create your models here.
class URLModel(models.Model):
    url = models.URLField(max_length=1024)
    tenwords = models.TextField()
    wordcount = models.TextField()

    def __str__(self):
        return self.url
    