from django.db import models

class URLTransform(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=10, unique=True)
    expiration_date = models.DateTimeField()

    def __str__(self):
        return self.original_url