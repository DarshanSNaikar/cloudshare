from django.db import models
from django.contrib.auth.models import User


class Media(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # text / image / video
    type = models.CharField(max_length=10)

    text_content = models.TextField(blank=True, null=True)

    file_url = models.URLField(blank=True, null=True)

    # share link will be created later
    share_code = models.CharField(max_length=10, unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)