from django.db import models


class WorkSpace(models.Model):

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
