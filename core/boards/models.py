from django.db import models


class Board(models.Model):

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    
