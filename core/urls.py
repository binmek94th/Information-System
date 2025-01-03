from django.urls import path
from core import views

urlpatterns = [
    path('student/', views.student, name='student'),
    path('department/', views.department, name='department'),
]