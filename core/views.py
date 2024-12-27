from django.shortcuts import render
from .forms import StudentRegistrationForm, DepartmentRegistrationForm


def department(request):
    if request == 'POST':
        form = DepartmentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = DepartmentRegistrationForm()
        return render(request, 'department.html', {'form': form})


def student_registration(request):
    if request == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StudentRegistrationForm()
        return render(request, 'student-registration.html', {'form': form})
