from django.urls import path
from core import views

urlpatterns = [
    path('student_registration/', views.student_registration, name='student_registration'),
    path('department/', views.department, name='department'),
]