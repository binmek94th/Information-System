from core.models import Student, Department, Instructor, Course, DepartmentHead, Term, Section, CourseOffering,Grade
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
    first_name = forms.CharField(max_length=255, label="First Name", widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student first name'}))
    last_name = forms.CharField(max_length=255, label="Last Name", widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student last name'}))
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    country = forms.CharField(max_length=255, label="Country", widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student country'}))
    city = forms.CharField(max_length=255, label="City", widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student city'}))
    street = forms.CharField(max_length=255, label="Street", widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student street'}))
    phone_number = forms.CharField(max_length=12, label="Phone Number", widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student phone number'}))
    email = forms.EmailField( label="Email", widget=forms.EmailInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student email'}))
    department= forms.ModelChoiceField(queryset=Department.objects.all(), label="Department", widget=forms.Select(attrs={'class': 'form-control col-sm-12 col-md-6'}))
    guardian_first_name = forms.CharField(label="Guardian's First Name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student guardian First Name'}))
    guardian_last_name = forms.CharField(label="Guardian's Last Name", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student guardian Last Name'}))
    guardian_phone_number = forms.CharField(label="Guardian's Phone Number", max_length=12, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student guardian phone number'}))
    guardian_address = forms.CharField(label="Guardian's Address", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter student guardian address'}))
    year_of_study = forms.IntegerField(label="Year of Study", widget=forms.NumberInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter year of study'}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label="Section", widget=forms.Select(attrs={'class': 'form-control col-sm-12 col-md-6'}))
    
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['is_verified', 'joined_at', 'is_deleted', 'user', 'id', 'student_id']

    def __init__(self, *args, **kwargs):
        department_queryset = kwargs.pop('department_queryset', None)
        super().__init__(*args, **kwargs)
        if department_queryset:
            self.fields['department'].queryset = department_queryset

    



def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for myField in self.fields:
        self.fields[myField].widget.attrs['class'] = 'form-control'
class InstructorRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter your last name'}))
    country = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter your country'}))
    city = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter your city'}))
    street = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter your street'}))
    phone_number = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter your phone number'}))
    email = forms.EmailField( widget=forms.EmailInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter your email'}))
    department= forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'form-control col-sm-12 col-md-6'}))
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
  
    name= forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-md-6', 'placeholder': 'Enter course name'}))
    code = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-md-6', 'placeholder': 'Enter course code'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control  col-md-6', 'placeholder': 'Enter course description'}))
        
    
    
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
        widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'DD-MM-YYYY', 'class': 'form-control'})
    )
    name= forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter term name'}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter year'}))
    class Meta:
        model = Term
        fields = '__all__'
        exclude = ['id', 'is_deleted']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control col-sm-12 col-md-6', 'placeholder': 'Enter section name'}))
        department= forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'form-control col-sm-12 col-md-6'}))
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
class Gradeform(forms.ModelForm):
    class Meta:
        model = Grade
        fields='__all__'
        exclude=['id']
        