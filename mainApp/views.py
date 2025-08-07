from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from . import serializers, models
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from datetime import datetime
from rest_framework.parsers import MultiPartParser, FormParser
from supabase import create_client
import mimetypes
import os
import requests
import urllib.parse
from datetime import datetime
from accounts.authentication import FirebaseAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_BUCKET = "attachments"
SUPABASE_KEY =  os.getenv("SUPABASE_SERVICE_ROLE")

from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

class TaskAPI(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request, id=None):
        if id:
            task = get_object_or_404(models.Task, id=id, user=request.user)
            serializer = serializers.TaskSerializer(task)
            return Response({"status": "success", "payload": serializer.data}, status=status.HTTP_200_OK)
        try:
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
                supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                safe_file_name = urllib.parse.quote(f"{timestamp}_{file.name}")
                file_path = f"{request.user.id}/{safe_file_name}"


                # Read raw file bytes (important!)
                file_bytes = file.read()

                content_type = file.content_type
                if content_type == 'multipart/form-data':
                    guessed_type, _ = mimetypes.guess_type(file.name)
                    content_type = guessed_type or 'application/octet-stream'

                
                # Upload to Supabase
                res = supabase.storage.from_("attachments").upload(
                    path=file_path,
                    file=file_bytes,  # ✅ raw bytes, NOT request object
                    file_options={"content-type": content_type}
                )

                # if hasattr(res, 'error') and res.error:
                #     return Response({"status": "error", "message": str(res.error)}, status=500)
                if isinstance(res, dict) and res.get("error"):
                    return Response({"status": "error", "message": res['error']['message']}, status=500)

                file_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_path}"
                # print("Generated file URL:", file_url)
            
            task_data = {
                "title": request.data.get("title"),
                "description": request.data.get("description"),
                "completed": request.data.get("completed"),
                "priority": request.data.get("priority"),     # optional
                "repeat": request.data.get("repeat"),         # optional
                "category": request.data.get("category"),     # optional
                "due_date": request.data.get("due_date"),     # optional
            }


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
        if id:
            task = get_object_or_404(models.Task, id=id, user=request.user)
            serializer = serializers.TaskSerializer(task, data=request.data, partial=True)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "payload": serializer.data}, status=status.HTTP_200_OK)
            return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except models.Task.DoesNotExist:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id=None):
        if id:
            task = get_object_or_404(models.Task, id=id, user=request.user)
        try:
            task.delete()
            return Response({"status": "success", "message": "Task deleted"}, status=status.HTTP_200_OK)

        except models.Task.DoesNotExist:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
