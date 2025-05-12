from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.

class TaskAPI(APIView):
    def get(self, request, id=None):
        if id:
            task = models.Task.objects.get(id=id)
            serializer = serializers.TaskSerializer(task)
            return Response({"status":"success", "payload": serializer.data}, status=status.HTTP_200_OK)
        tasks = models.Task.objects.all()
        serializer = serializers.TaskSerializer(tasks, many=True)
        return Response({"status":"success", "payload": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            serializer = serializers.TaskSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"status":"error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"status":"success", "payload": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status":"error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id=None):
        try:
            task = models.Task.objects.get(id=id)
            # task = models.Task.objects.get(id=request.data['id'])
            serializer = serializers.TaskSerializer(task, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({"status":"error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"status":"success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id=None):
        try:
            task = models.Task.objects.get(id=id)
            # task = models.Task.objects.get(id=request.data['id'])
            task.delete()
            return Response({"status":"success", "message": "Task deleted"}, status=status.HTTP_200_OK)
        except models.Task.DoesNotExist:
            return Response({"status":"error", "error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status":"error", "data": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
