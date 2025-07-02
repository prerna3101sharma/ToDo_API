from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from . import serializers, models
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

class TaskAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None):
        try:
            if id:
                task = get_object_or_404(models.Task, id=id, user=request.user)
                serializer = serializers.TaskSerializer(task)
                return Response({"status": "success", "payload": serializer.data}, status=status.HTTP_200_OK)

            tasks = models.Task.objects.filter(user=request.user)
            serializer = serializers.TaskSerializer(tasks, many=True)
            return Response({"status": "success", "payload": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = serializers.TaskSerializer(data=request.data)
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
