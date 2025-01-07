from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm, DepartmentRegistrationForm, InstructorRegistrationForm, \
    CourseRegistrationForm, LoginForm
from .models import Department, Student, User, Instructor, Course
from .utils import generate_easy_password
from django.contrib.auth import logout

def login(request):
    login_form = LoginForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    if user.is_active:
                        auth_login(request, user)

                        if user.role == 'artist':
                            return redirect('artist_page')
                        elif user.role == 'buyer':
                            return redirect('home')
                    else:
                        messages.error(request, "Your account is inactive. Please contact support.")
                else:
                    messages.error(request, "Invalid username or password.")

    if request.method == 'GET' and 'signout' in request.GET:
        logout(request)
        messages.success(request, "You have successfully signed out.")
        return redirect('home')

    return render(request, 'login.html', {
        'login_form': login_form,
    })


def department(request):
    departmentDb = Department.objects.filter(is_deleted=False)
    form = DepartmentRegistrationForm()
    context = {'departmentDb': departmentDb, 'form': form}
    if request.method == 'POST' and ('_method' not in request.POST or request.POST['_method'] != 'PUT'):
        if 'id' in request.POST:
            departmentDb = Department.objects.get(id=request.POST['id'])
            departmentDb.is_deleted = True
            departmentDb.is_active = False
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


def student(request):
    studentDb = Student.objects.filter()
    department_queryset = Department.objects.filter(is_active=True).filter(is_deleted=False)
    form = StudentRegistrationForm(department_queryset=department_queryset)
    context = {'studentDb': studentDb, 'form': form}
    if request.method == 'POST' and ('_method' not in request.POST or request.POST['_method'] != 'PUT'):
        if 'id' in request.POST:
            studentDb = Student.objects.get(id=request.POST['id'])
            studentDb.is_deleted = True
            studentDb.save()
            return render(request, 'student.html', {'context': context}, status=400)
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student_id = Student.objects.count() + 1 + 1000
            passwordGenerated = generate_easy_password(6)
            user = User.objects.create_user(
                username=str(student_id),
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                password=passwordGenerated,
                country=request.POST['country'],
                city=request.POST['city'],
                street=request.POST['street'],
                phone_number=request.POST['phone_number'],
            )
            studentNew = {
                'student_id': student_id,
                'user': user,
                'department': form.cleaned_data['department'],
                'year_of_study': form.cleaned_data['year_of_study'],
                'guardian_first_name': form.cleaned_data['guardian_first_name'],
                'guardian_last_name': form.cleaned_data['guardian_last_name'],
                'guardian_phone_number': form.cleaned_data['guardian_phone_number'],
                'guardian_address': form.cleaned_data['guardian_address'],
            }
            Student.objects.create(**studentNew)
            return render(request, 'student.html', {'context': context}, status=201)
        else:
            return render(request, 'student.html', {'context': context}, status=204)
    if request.method == 'POST' and request.POST['_method'] == 'PUT':
        studentDb = Student.objects.get(id=request.POST['id'])
        studentUser = User.objects.get(id=studentDb.user.id)
        form = StudentRegistrationForm(request.POST, instance=studentDb)
        if form.is_valid():
            studentUser.first_name = form.cleaned_data['first_name']
            studentUser.last_name = form.cleaned_data['last_name']
            studentUser.email = form.cleaned_data['email']
            studentUser.country = form.cleaned_data['country']
            studentUser.city = form.cleaned_data['city']
            studentUser.street = form.cleaned_data['street']
            studentUser.phone_number = form.cleaned_data['phone_number']
            studentDb.is_active = form.cleaned_data['is_active']
            studentDb.guardian_first_name = form.cleaned_data['guardian_first_name']
            studentDb.guardian_last_name = form.cleaned_data['guardian_last_name']
            studentDb.guardian_address = form.cleaned_data['guardian_address']
            studentDb.guardian_phone_number = form.cleaned_data['guardian_phone_number']

            studentUser.save()
            studentDb.save()

            return render(request, 'student.html', {'context': context}, status=201)
        else:
            print("printing", context.studentDb)
            return render(request, 'student.html', {'context': context}, status=204)
    if request.method == 'GET':
        return render(request, 'student.html', {'context': context})


def instructor(request):
    InstructorDb = Instructor.objects.filter(is_deleted=False)
    department_queryset = Department.objects.filter(is_active=True).filter(is_deleted=False)
    form = InstructorRegistrationForm(department_queryset=department_queryset)
    context = {'InstructorDb': InstructorDb, 'form': form}
    if request.method == 'POST' and ('_method' not in request.POST or request.POST['_method'] != 'PUT'):
        if 'id' in request.POST:
            instructorDb = Instructor.objects.get(id=request.POST['id'])
            instructorDb.is_deleted = True
            instructorDb.save()
            return render(request, 'instructor.html', {'context': context}, status=202)
        form = InstructorRegistrationForm(request.POST)
        if form.is_valid():
            instructor_id = "IN" + str(Instructor.objects.count() + 1 + 1000)
            passwordGenerated = generate_easy_password(6)
            user = User.objects.create_user(
                username=str(instructor_id),
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                password=passwordGenerated,
                country=request.POST['country'],
                city=request.POST['city'],
                street=request.POST['street'],
                phone_number=request.POST['phone_number'],
            )
            instructorNew = {
                'instructor_id': instructor_id,
                'user': user,
                'department': form.cleaned_data['department'],
            }
            Instructor.objects.create(**instructorNew)
            return render(request, 'instructor.html', {'context': context}, status=201)
        else:
            return render(request, 'instructor.html', {'context': context}, status=204)
    if request.method == 'POST' and request.POST['_method'] == 'PUT':
        instructorDb = Instructor.objects.get(id=request.POST['id'])
        instructorUser = User.objects.get(id=instructorDb.user.id)
        form = StudentRegistrationForm(request.POST, instance=instructorDb)
        if form.is_valid():
            instructorUser.first_name = form.cleaned_data['first_name']
            instructorUser.last_name = form.cleaned_data['last_name']
            instructorUser.email = form.cleaned_data['email']
            instructorUser.country = form.cleaned_data['country']
            instructorUser.city = form.cleaned_data['city']
            instructorUser.street = form.cleaned_data['street']
            instructorUser.phone_number = form.cleaned_data['phone_number']
            instructorDb.is_active = form.cleaned_data['is_active']

            instructorUser.save()
            instructorDb.save()

            return render(request, 'instructor.html', {'context': context}, status=201)
        else:
            return render(request, 'instructor.html', {'context': context}, status=204)
    if request.method == 'GET':
        return render(request, 'instructor.html', {'context': context})


def course(request):
    courseDb = Course.objects.filter(is_deleted=False)
    form = CourseRegistrationForm()
    context = {'CourseDb': courseDb, 'form': form}
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if request.method == 'POST' and ('_method' not in request.POST or request.POST['_method'] != 'PUT'):
        if 'id' in request.POST:
            courseDb = Course.objects.get(id=request.POST['id'])
            courseDb.is_deleted = True
            courseDb.save()
            return render(request, 'course.html', {'context': context}, status=202)
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'course.html', {'context': context}, status=201)
        else:
            return render(request, 'course.html', {'context': context}, status=204)
    if request.method == 'POST' and request.POST['_method'] == 'PUT':
        courseDb = Course.objects.get(id=request.POST['id'])
        form = DepartmentRegistrationForm(request.POST, instance=courseDb)
        if form.is_valid():
            form.save()
            return render(request, 'course.html', {'context': context}, status=201)
        else:
            return render(request, 'course.html', {'context': context}, status=204)

    if request.method == 'GET':
        print(context)
        return render(request, 'course.html', {'context': context})