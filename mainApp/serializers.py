from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'priority', 'due_date']
        # exclude = ['created_at', 'updated_at']