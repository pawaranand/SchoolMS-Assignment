# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime
from django.utils.translation import ugettext as _

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

class UserType(models.Model):
    user_type = models.CharField(max_length=100, primary_key=True)


GENDER_CHOICES = (
    (1, _("Male")),
    (2, _("Female"))
)

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    email = models.EmailField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)

    city = models.CharField(max_length=100, null=True)

    def __str__(self):
        if self.first_name and not self.last_name:
            return self.first_name
        elif self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return 'Parent'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE,null=True , blank=True)

    def __str__(self):
        if self.first_name and not self.last_name:
            return self.first_name
        elif self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return 'Student'
    
    def get_unanswered_questions(self, exam):
        answered_questions = self.exam_question_logs \
            .filter(exam=exam) \
            .values_list('question__pk', flat=True)
        questions = exam.questions.exclude(pk__in=answered_questions).order_by('question_text')
        return questions

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    city = models.CharField(max_length=100, null=True)
    qualification = models.CharField(max_length=100, null=True)

    def __str__(self):
        if self.first_name and not self.last_name:
            return self.first_name
        elif self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return 'Teacher'

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        if self.department_name:
            return self.department_name
        else:
            return 'Department'

class Course(models.Model):
    course = models.CharField(max_length=100)
    dept_description = models.CharField(max_length=200, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)    

    def __str__(self):
        if self.course:
            return self.course
        else:
            return 'Course'

class Subject(models.Model):
    subject = models.CharField(max_length=100)
    subject_description = models.CharField(max_length=200, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='subjects')

    def __str__(self):
        if self.subject:
            return self.subject
        else:
            return 'Subject'

class Exam(models.Model):
    exam_name = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=200, null=True,blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='exams')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='exams')
    

    def __str__(self):
        if self.exam_name:
            return self.exam_name
        else:
            return 'Exam'


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,null=True,related_name='questions')
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    weightage = models.IntegerField(default=5)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?' 


class StudentCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='student_courses')

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='exam_results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='exam_results')
    score = models.FloatField(null=True)
    evaluated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True) 

class ExamLog(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='exam_question_logs')
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='exam_question_logs')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    weightage = models.IntegerField(default=5)
    score = models.FloatField(null=True)
    evaluated = models.BooleanField(default=False)
    answer = models.CharField(max_length=200,default=False)
    date = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='student_attendances')
    attendance_date = models.DateField('attendance date')
    attendance_status = models.BooleanField('Present',default=False)
    reason_for_absentee = models.CharField(max_length=200, null=True, blank=True)
    attendance_marked_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)     

