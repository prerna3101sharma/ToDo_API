from django.urls import path
from .views import health_check
from .views import *

urlpatterns = [
    path("tasks/", TaskAPI.as_view()),
    path("tasks/<int:id>", TaskAPI.as_view()),
    path('ping/', health_check),
    path('progress/', ProgressAPI.as_view()),    
]
