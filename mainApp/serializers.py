from rest_framework import serializers
from .models import *
import mimetypes


class TaskSerializer(serializers.ModelSerializer):
    attachment = serializers.URLField(required=False, allow_null=True)
    due_date = serializers.DateTimeField(
        required=False,
        allow_null=True,
        format="%Y-%m-%d %H:%M",           # Optional: response format
        input_formats=["%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"]  # Accept both "2025-08-07 14:30" and "2025-08-07T14:30"
    )
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'priority', 'due_date']
        # exclude = ['created_at', 'updated_at']

        extra_kwargs = {
            'user': {'read_only': True}  # ✅ Don't expect this in request
        }



