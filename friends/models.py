from django.db import models
from accounts.models import *

# Create your models here.
class FriendRequest(models.Model):
    """
    Model that stores friendrequest information
    """
    Status_Choices = ( 
    ("pending", "pending"),
    ("accepted", "accepted"),
    ('rejected', 'rejected'),
      )
    request_from = models.ForeignKey(CustomUser, related_name='request_from', on_delete=models.CASCADE) 
    request_to = models.ForeignKey(CustomUser, related_name='request_to', on_delete=models.CASCADE)
    status = models.CharField(choices=Status_Choices, default='pending', max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
    class Meta:
        verbose_name = 'FriendRequest Model'