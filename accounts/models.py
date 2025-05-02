from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='photographer_profile')
    bio = models.TextField(blank=True)
    phone_number= models.CharField(max_length=15, blank=True)
    specialization = models.CharField(max_length=255,  blank=True, help_text="Comma separated list of specializations")
    profession = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
    # class Meta:
    #     ordering = ['user__username']
        
