from core.models import Student, Department, Instructor, Course, DepartmentHead, Term, Section, CourseOffering
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class DepartmentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        exclude = ['id', 'is_deleted']


class DepartmentHeadForm(forms.ModelForm):
    class Meta:
        model = DepartmentHead
        fields = '__all__'
        exclude = ['id', 'is_deleted']

    def __init__(self, *args, **kwargs):
        department_queryset = kwargs.pop('department_queryset', None)
        instructor_queryset = kwargs.pop('instructor_queryset', None)
        super().__init__(*args, **kwargs)
        if instructor_queryset:
            self.fields['instructor'].queryset = instructor_queryset
        if department_queryset:
            self.fields['department'].queryset = department_queryset


class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    street = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=12)
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['is_verified', 'joined_at', 'is_deleted', 'user', 'id', 'student_id']

    def __init__(self, *args, **kwargs):
        department_queryset = kwargs.pop('department_queryset', None)
        super().__init__(*args, **kwargs)
        if department_queryset:
            self.fields['department'].queryset = department_queryset


class InstructorRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    street = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=12)
    email = forms.EmailField()

    class Meta:
        model = Instructor
        fields = '__all__'
        exclude = ['is_verified', 'joined_at', 'is_deleted', 'user', 'id', 'instructor_id']

    def __init__(self, *args, **kwargs):
        department_queryset = kwargs.pop('department_queryset', None)
        super().__init__(*args, **kwargs)
        if department_queryset:
            self.fields['department'].queryset = department_queryset


class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['id', 'is_deleted', 'department']

    def save(self, department=None, *args, **kwargs):
        instance = super().save(commit=False)
        if department:
            instance.department = department
        instance.save()
        return instance


class TermForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY'})
    )
    end_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY'})
    )

    class Meta:
        model = Term
        fields = '__all__'
        exclude = ['id', 'is_deleted']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
        exclude = ['id', 'is_deleted']

    def __init__(self, *args, **kwargs):
        department_queryset = kwargs.pop('department_queryset', None)
        super().__init__(*args, **kwargs)
        if department_queryset:
            self.fields['department'].queryset = department_queryset


class CourseOfferingForm(forms.ModelForm):
    class Meta:
        model = CourseOffering
        fields = '__all__'
        exclude = ['id', 'is_deleted', 'department']

    def __init__(self, *args, **kwargs):
        course_queryset = kwargs.pop('course', None)
        term_queryset = kwargs.pop('term', None)
        super().__init__(*args, **kwargs)
        if course_queryset:
            self.fields['term'].queryset = term_queryset
