from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from .models import (Question, Student, Teacher,
                              Subject, User,Attendance,ExamLog,Exam,Parent)

USER_CHOICES = (('1', 'Student',), ('2', 'Teacher',),('3', 'Parent',))

class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(widget=forms.RadioSelect, choices=USER_CHOICES)
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.CharField(label='Email')

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        print(self.cleaned_data["password1"])
        user = super(UserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if int(self.cleaned_data.get('user_type')) == 1:
            user.is_student = True
        elif int(self.cleaned_data.get('user_type')) == 2:
            user.is_teacher = True
        elif int(self.cleaned_data.get('user_type')) == 3:
            user.is_parent = True

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        user.save()
        
        if int(self.cleaned_data.get('user_type')) == 1:
            student = Student.objects.create(user=user,
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get('last_name'),
                    email = self.cleaned_data.get('email')
                )
        
        elif int(self.cleaned_data.get('user_type')) == 2:
            teacher = Teacher.objects.create(user=user,
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email = self.cleaned_data.get('email')
            )
        
        elif int(self.cleaned_data.get('user_type')) == 3:
            parent = Parent.objects.create(user=user,
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email = self.cleaned_data.get('email')
            )
       
        return user

class DateInput(forms.DateInput):
    input_type = 'date'

class AddAttendenceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('student', 'attendance_date','attendance_status','reason_for_absentee' )
        widgets = {'attendance_date': DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def clean(self):
        super().clean()
        attn_date = self.cleaned_data.get('attendance_date')
        student = self.cleaned_data.get('student')
        attn_id = self.instance.pk
        if Attendance.objects.exclude(pk=attn_id).filter(attendance_date=attn_date,student=student).exists():
            raise forms.ValidationError(u'Attendance for "%s" is already added.' % attn_date)
        return attn_id


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text','weightage' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        question = self.cleaned_data.get('question_text')
        question_id = self.instance.pk
        if Question.objects.exclude(pk=question_id).filter(question_text=question).exists():
            raise forms.ValidationError(u'Question "%s" is already in use.' % question)
        return question_id


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('exam_name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_exam_name(self):
        super().clean()
        exam_name = self.cleaned_data.get('exam_name')
        exam = self.instance.pk
        if Exam.objects.exclude(pk=exam).filter(exam_name=exam_name).exists():
            raise forms.ValidationError(u'Exam Name "%s" is already in use.' % exam_name)
        return exam_name        

class TakeExamForm(forms.ModelForm):
    answer = forms.CharField(widget=forms.Textarea,required=True)

    class Meta:
        model = ExamLog
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)

class EvaluateExamForm(forms.ModelForm):

    class Meta:
        model = ExamLog
        fields = ('score', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
