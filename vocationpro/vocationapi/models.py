from django.db import models
from django.contrib.auth.models import User

# Create your models herc
class employee(models.Model):
    choices = (
        ('pending',"PENDING"),
        ('approved',"APPROVED"),
        ('rejected',"REJECTED")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    start_date = models.CharField(max_length=500)
    end_date = models.CharField(max_length=500)
    r_date = models.CharField(max_length=500)
    status = models.CharField(max_length=500,default='Pending',choices=choices)
    total_v = models.IntegerField(default=30)