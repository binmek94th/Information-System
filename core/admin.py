from django.contrib import admin


# Register your models here.
from .models import (Student,Section,Instructor,Department,DepartmentHead,Course,CourseOffering,Term)
admin.site.register(Student)
admin.site.register(Section)
admin.site.register(Instructor)
admin.site.register(Department)
admin.site.register(DepartmentHead)
admin.site.register(Course)
admin.site.register(CourseOffering)