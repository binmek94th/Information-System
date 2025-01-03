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
    country = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    street = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=12)
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['is_verified', 'is_active', 'joined_at', 'user', 'id', 'student_id']

    def __init__(self, *args, **kwargs):
        department_queryset = kwargs.pop('department_queryset', None)
        super().__init__(*args, **kwargs)
        if department_queryset:
            self.fields['department'].queryset = department_queryset
