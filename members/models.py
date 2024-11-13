from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# Create your models here.

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    dateofbirth = models.DateField(null = True, blank = True)
    bio = models.TextField(null = True, blank = True, max_length= 5000)

    def __str__(self) -> str:
        return self.user.get_short_name()
    
    def get_items(self) -> str:
        items = self.items.all()
        if items.exists():
            links = []
            for item in items:
                url = f'/admin/items/item/{item.id}/change/'
                links.append(format_html('<a href="{}">{}</a>', url, item.name))
            return mark_safe(', '.join(links))
        return 'No items'
    
class Score(models.Model):
    rated_user = models.ForeignKey(User, related_name='received_scores', on_delete=models.CASCADE)
    rater_user = models.ForeignKey(User, related_name='given_scores', on_delete=models.CASCADE)
    score = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rated_user', 'rater_user') 

    def __str__(self):
        return f'{self.rater_user} rated {self.rated_user} with {self.score}'