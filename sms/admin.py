# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Register your models here.
from django.contrib import admin

from .models import Question, Student, Parent, Department, Course, Attendance,\
 StudentCourse, Subject, Teacher, Exam

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['exam','question_text',]}),
	]
	#inlines = [ChoiceInline]
	
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(StudentCourse)
admin.site.register(Teacher)
admin.site.register(Exam)
