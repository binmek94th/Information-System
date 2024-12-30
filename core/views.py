from django.shortcuts import render
from .forms import StudentRegistrationForm, DepartmentRegistrationForm
from .models import Department


def department(request):
    departmentDb = Department.objects.filter(is_deleted=False)
    form = DepartmentRegistrationForm()
    context = {'departmentDb': departmentDb, 'form': form}
    if request.method == 'POST' and ('_method' not in request.POST or request.POST['_method'] != 'PUT'):
        if 'id' in request.POST:
            departmentDb = Department.objects.get(id=request.POST['id'])
            departmentDb.is_deleted = True
            departmentDb.save()
            return render(request, 'department.html', {'context': context}, status=400)
        form = DepartmentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'department.html', {'context': context}, status=201)
        else:
            return render(request, 'department.html', {'context': context}, status=204)
    if request.method == 'POST' and request.POST['_method'] == 'PUT':
        departmentDb = Department.objects.get(id=request.POST['id'])
        form = DepartmentRegistrationForm(request.POST, instance=departmentDb)
        if form.is_valid():
            form.save()
            return render(request, 'department.html', {'context': context}, status=201)
        else:
            return render(request, 'department.html', {'context': context}, status=204)
    if request.method == 'GET':
        return render(request, 'department.html', {'context': context})


def student_registration(request):
    if request == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StudentRegistrationForm()
        return render(request, 'student-registration.html', {'form': form})
