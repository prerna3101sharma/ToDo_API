from rest_framework import serializers
from .models import *
import mimetypes


# Custom file field to validate and fix file content type
class AttachmentUploadField(serializers.FileField):
    def to_internal_value(self, file):
        try:
            # Block invalid content types
            if file.content_type == 'multipart/form-data':
                raise serializers.ValidationError("Invalid file content type: multipart/form-data")

            # Guess and fix broken content types
            if not file.content_type or '/' not in file.content_type:
                guessed_type, _ = mimetypes.guess_type(file.name)
                file.content_type = guessed_type or 'application/octet-stream'

            return super().to_internal_value(file)

        except AttributeError as e:
            raise serializers.ValidationError(f"Invalid file object: {str(e)}")

        except Exception as e:
            raise serializers.ValidationError(f"File processing failed: {str(e)}")

class TaskSerializer(serializers.ModelSerializer):
    attachment = AttachmentUploadField(required=False, allow_null=True)
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'priority', 'due_date']
        # exclude = ['created_at', 'updated_at']

        extra_kwargs = {
            'user': {'read_only': True}  # ✅ Don't expect this in request
        }



