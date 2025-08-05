from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from . import serializers, models
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from datetime import datetime
from rest_framework.parsers import MultiPartParser, FormParser
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY =  os.getenv("SUPABASE_SERVICE_ROLE")

class TaskAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request, id=None):
        try:
            if id:
                task = get_object_or_404(models.Task, id=id, user=request.user)
                serializer = serializers.TaskSerializer(task)
                return Response({"status": "success", "payload": serializer.data}, status=status.HTTP_200_OK)
            category = request.query_params.get('category')
            tasks = models.Task.objects.filter(user=request.user)
            # Filter by category
            if category:
                tasks = tasks.filter(category__iexact=category)

            # Filter by date range
            start_date = request.query_params.get('start')
            end_date = request.query_params.get('end')
            if start_date and end_date:
                try:
                    start = datetime.strptime(start_date, "%Y-%m-%d").date()
                    end = datetime.strptime(end_date, "%Y-%m-%d").date()
                    tasks = tasks.filter(created_at__range=(start, end))
                except ValueError:
                    return Response(
                        {"status": "error", "error": "Invalid date format. Use YYYY-MM-DD."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            serializer = serializers.TaskSerializer(tasks, many=True)
            return Response({"status": "success", "payload": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get('attachment')
            file_url = None
    
            if file:
                # Initialize Supabase client
                supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
                # Upload to Supabase bucket
                file_path = f"{request.user.id}/{file.name}"
                res = supabase.storage.from_("attachments").upload(
                    path=file_path,
                    file=file.read(),
                    file_options={"content-type": file.content_type}
                )
    
                if res.get("error"):
                    return Response({"status": "error", "message": res['error']['message']}, status=500)
    
                # Construct public URL
                file_url = f"{SUPABASE_URL}/storage/v1/object/public/attachments/{file_path}"
    
            # Create a copy of request data with 'attachment' as URL
            task_data = request.data.copy()
            if file_url:
                task_data['attachment'] = file_url
    
            serializer = serializers.TaskSerializer(data=task_data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"status": "success", "payload": serializer.data}, status=status.HTTP_201_CREATED)
    
            return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
        except ValidationError as ve:
            return Response({"status": "error", "message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, id=None):
        try:
            task = get_object_or_404(models.Task, id=id, user=request.user)
            serializer = serializers.TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "payload": serializer.data}, status=status.HTTP_200_OK)
            return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except models.Task.DoesNotExist:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id=None):
        try:
            task = get_object_or_404(models.Task, id=id, user=request.user)
            task.delete()
            return Response({"status": "success", "message": "Task deleted"}, status=status.HTTP_200_OK)

        except models.Task.DoesNotExist:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
