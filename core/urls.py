from django.urls import path
from core import views

urlpatterns = [
    path('student/', views.student, name='student'),
    path('department/', views.department, name='department'),
    path('department_head/', views.department_head, name='department_head'),
    path('instructor/', views.instructor, name='department'),
    path('course/', views.course, name='course'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('permission_denied/', views.permission_denied, name='permission_denied'),
]
