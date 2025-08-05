from django.db import models
from django.conf import settings

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority_choices = [
        ('low', 'Low'),
        ('medium', 'Medium'), 
        ('high', 'High'),
    ]
    priority = models.CharField(max_length=6, choices=priority_choices, default='medium')
    repeat_choices = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    repeat = models.CharField(max_length=10, choices=repeat_choices, default='none')

    category_choices = [
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('health', 'Health'),  
        ('finance', 'Finance'),
        ('study', 'Study'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=10, choices=category_choices, default='other')
    attachment = models.URLField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True) 


    def __str__(self):
        return self.title
