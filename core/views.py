from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentRegistrationForm, DepartmentRegistrationForm, InstructorRegistrationForm, \
    CourseRegistrationForm, LoginForm, DepartmentHeadForm, TermForm, SectionForm
from .models import Department, Student, User, Instructor, Course, DepartmentHead, Term, Section
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

                        # if user.role == 'artist':
                        #     return redirect('artist_page')
                        # elif user.role == 'buyer':
                        #     return redirect('home')
                    else:
                        messages.error(request, "Your account is inactive. Please contact support.")
                else:
                    messages.error(request, "Invalid username or password.")

    if request.method == 'GET' and 'sign_out' in request.GET:
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
        data = request.POST.copy()
        data['is_active'] = str('is_active' in data)
        form = DepartmentRegistrationForm(data)
        if form.is_valid():
            form.save()
            return render(request, 'department.html', {'context': context}, status=201)
        else:
            return render(request, 'department.html', {'context': context}, status=204)
    if request.method == 'POST' and request.POST['_method'] == 'PUT':
        departmentDb = Department.objects.get(id=request.POST['id'])
        data = request.POST.copy()
        data['is_active'] = str('is_active' in data)
        form = DepartmentRegistrationForm(data, instance=departmentDb)
        if form.is_valid():
            form.save()
            return render(request, 'department.html', {'context': context}, status=201)
        else:
            return render(request, 'department.html', {'context': context}, status=204)
    if request.method == 'GET':
        return render(request, 'department.html', {'context': context})


def department_head(request):
    head = DepartmentHead.objects.filter(is_deleted=False)
    department_queryset = Department.objects.filter(is_active=True).filter(is_deleted=False)
    instructor_queryset = Instructor.objects.filter(is_active=True).filter(is_deleted=False)
    form = DepartmentHeadForm(department_queryset=department_queryset, instructor_queryset=instructor_queryset)
    context = {'head': head, 'form': form}
    if request.method == 'POST' and ('_method' not in request.POST or request.POST['_method'] != 'PUT'):
        if 'id' in request.POST:
            headDb = DepartmentHead.objects.get(id=request.POST['id'])
            headDb.is_deleted = True
            headDb.is_active = False
            headDb.save()
            return render(request, 'department_head.html', {'context': context}, status=400)
        form = DepartmentHeadForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'department_head.html', {'context': context}, status=201)
        else:
            return render(request, 'department_head.html', {'context': context}, status=204)
    if request.method == 'POST' and request.POST['_method'] == 'PUT':
        headDb = DepartmentHead.objects.get(id=request.POST['id'])
        form = DepartmentHeadForm(request.POST, instance=headDb)
        if form.is_valid():
            form.save()
            return render(request, 'department_head.html', {'context': context}, status=201)
        else:
            return render(request, 'department_head.html', {'context': context}, status=204)
    if request.method == 'GET':
        return render(request, 'department_head.html', {'context': context})


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
            student_id = 'ST' + str(Student.objects.count() + 1 + 1000)
            user = create_user(request, student_id)
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


def create_user(request, created_id):
    passwordGenerated = generate_easy_password(8)
    user = User.objects.create_user(
        username=created_id,
        email=request.POST['email'],
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        password=passwordGenerated,
        country=request.POST['country'],
        city=request.POST['city'],
        street=request.POST['street'],
        phone_number=request.POST['phone_number'],
    )
    return user


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
            created_id = 'IN' + str(Instructor.objects.count() + 1 + 1000)
            user = create_user(request, created_id)
            instructorNew = {
                'instructor_id': created_id,
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


def permission_denied(request):
    return render(request, 'permission_denied.html')


def course(request):
    courseDb = Course.objects.filter(is_deleted=False)
    form = CourseRegistrationForm()
    context = {'courseDb': courseDb, 'form': form}
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if not user.groups.filter(name="Department Head").exists():
        return redirect('permission_denied')
    if request.method == 'POST' and ('_method' not in request.POST or request.POST['_method'] != 'PUT'):
        if 'id' in request.POST:
            courseDb = Course.objects.get(id=request.POST['id'])
            courseDb.is_deleted = True
            courseDb.save()
            return render(request, 'course.html', {'context': context}, status=202)
        instructorDb = Instructor.objects.get(user=user)
        department_headDb = get_object_or_404(DepartmentHead, instructor=instructorDb)
        data = request.POST.copy()
        data['is_active'] = str('is_active' in data)
        form = CourseRegistrationForm(data)
        if form.is_valid():
            form.save(department=department_headDb.department)
            return render(request, 'course.html', {'context': context}, status=201)
        else:
            return render(request, 'course.html', {'form': form, 'errors': form.errors}, status=400)

    if request.method == 'POST' and request.POST['_method'] == 'PUT':
        courseDb = Course.objects.get(id=request.POST['id'])
        form = DepartmentRegistrationForm(request.POST, instance=courseDb)
        if form.is_valid():
            form.save()
            return render(request, 'course.html', {'context': context}, status=201)
        else:
            return render(request, 'course.html', {'context': context}, status=204)

    if request.method == 'GET':
        return render(request, 'course.html', {'context': context})


def term(request):
    termDb = Term.objects.filter(is_deleted=False)
    form = TermForm()
    context = {'termDb': termDb, 'form': form}
    if request.method == 'POST' and ('_method' not in request.POST or request.POST['_method'] != 'PUT'):
        if 'id' in request.POST:
            termDb = Term.objects.get(id=request.POST['id'])
            termDb.is_deleted = True
            termDb.is_active = False
            termDb.save()
            return render(request, 'term.html', {'context': context}, status=400)
        data = request.POST.copy()
        data['is_active'] = str('is_active' in data)
        form = TermForm(data)
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, 'term.html', {'context': context}, status=201)
        else:
            return render(request, 'term.html', {'context': context}, status=204)
    if request.method == 'POST' and request.POST['_method'] == 'PUT':
        termDb = Term.objects.get(id=request.POST['id'])
        form = TermForm(request.POST, instance=termDb)
        if form.is_valid():
            form.save()
            return render(request, 'term.html', {'context': context}, status=201)
        else:
            return render(request, 'term.html', {'context': context}, status=204)
    if request.method == 'GET':
        return render(request, 'term.html', {'context': context})


def section(request):
    sectionDb = Section.objects.filter(is_deleted=False)
    department_queryset = Department.objects.filter(is_active=True).filter(is_deleted=False)
    form = SectionForm(department_queryset=department_queryset)
    context = {'sectionDb': sectionDb, 'form': form}
    if request.method == 'POST' and ('_method' not in request.POST or request.POST['_method'] != 'PUT'):
        if 'id' in request.POST:
            sectionDb = Section.objects.get(id=request.POST['id'])
            sectionDb.is_deleted = True
            sectionDb.is_active = False
            sectionDb.save()
            return render(request, 'section.html', {'context': context}, status=400)
        data = request.POST.copy()
        data['is_active'] = str('is_active' in data)
        form = SectionForm(data)
        if form.is_valid():
            form.save()
            return render(request, 'section.html', {'context': context}, status=201)
        else:
            return render(request, 'section.html', {'context': context}, status=204)
    if request.method == 'POST' and request.POST['_method'] == 'PUT':
        sectionDb = Section.objects.get(id=request.POST['id'])
        form = SectionForm(request.POST, instance=sectionDb)
        if form.is_valid():
            form.save()
            return render(request, 'section.html', {'context': context}, status=201)
        else:
            return render(request, 'section.html', {'context': context}, status=204)
    if request.method == 'GET':
        return render(request, 'section.html', {'context': context})