from django.db import models
from members.models import Profile
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Sport(models.Model):
    name = models.CharField(null=False, blank=False, max_length=300)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
    
class ItemCondition(models.Model):
    name = models.CharField(null=False, blank=False, max_length=300)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name
    
class Item(models.Model):
    name = models.CharField(null=False, blank=False, max_length=300)
    sport = models.ForeignKey(Sport, related_name='items', on_delete=models.CASCADE)
    advertiser = models.ForeignKey(Profile, related_name='items', on_delete=models.CASCADE)
    description = models.TextField(null = True, blank= True, max_length=5000)
    price = models.FloatField(blank=False)
    createdate = models.DateField(null= True, blank=True)
    sold = models.BooleanField(default=False)
    image = models.ImageField(upload_to='uploads/item/', default='uploads/item/noimage.png')
    condition = models.ForeignKey(ItemCondition, related_name='items', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name