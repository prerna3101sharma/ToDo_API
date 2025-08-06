from rest_framework import serializers
from .models import *
import mimetypes


class TaskSerializer(serializers.ModelSerializer):
    attachment = serializers.URLField(required=False, allow_null=True)
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'priority', 'due_date']
        # exclude = ['created_at', 'updated_at']

        extra_kwargs = {
            'user': {'read_only': True}  # ✅ Don't expect this in request
        }



