from django.db import models

from renter.models import Renter
from local.models import Local

class Activity(models.Model):

    ACTIVITY_TYPE = (
        ("rent", "Rent a local"),
        ("unrent", "Unrent a local"),
        ("payment", "Payment of rent"),
    )

    type = models.CharField(max_length=20, choices=ACTIVITY_TYPE)
    act_at = models.DateTimeField(auto_now_add=True)

    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    made_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    work_space = models.ForeignKey("workspace.WorkSpace", on_delete=models.CASCADE, null=True)


class Notification(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(blank=True, null=True)
    work_space = models.ForeignKey("workspace.WorkSpace", on_delete=models.CASCADE, null=True)

    
