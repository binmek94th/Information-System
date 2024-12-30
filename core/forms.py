from core.models import Student, Department
from django import forms


class DepartmentRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=255)

    class Meta:
        model = Department
        fields = '__all__'
        exclude = ['id', 'is_deleted']


class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    birth_date = forms.DateField()

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['is_verified', 'is_active', 'joined_at', 'user', 'id', 'student_id']


