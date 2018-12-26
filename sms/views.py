# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib import messages
from .forms import SignUpForm,AddAttendenceForm, QuestionForm, TakeExamForm,ExamForm,EvaluateExamForm
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Avg, Count,Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import teacher_required,student_required,parent_required

from .models import Question, Student, Parent, Department, Course, Attendance,\
 StudentCourse, Subject, Teacher, Exam,ExamResult, User,ExamLog


from django.contrib.auth.views import login as auth_view_login
from django.contrib.auth.forms import AuthenticationForm


"""
    User Management Views
"""
def loginView(request):
    """
        param1 : username param2 : password
        Responsible for login and redirection  
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid)
        if form.is_valid():
            user = form.get_user()
            print(user)
            auth_view_login(request,user)
            if user.is_student:
                return redirect('sms:student_home')
            elif user.is_teacher:
                return redirect('sms:teacher_home')
            elif user.is_parent:
                return redirect('sms:parent_home')
    else:
        form = AuthenticationForm()
    return render(request,'registration/login.html',{'form':form})


def logoutView(request):
    """
        Responsible for clearing user session
    """
    user = request.user
    logout(request, user)
    return redirect("sms:home")

class SignUpView(CreateView):
    """
        param1 : username
        param2 : password1
        param3 : password2
        param4 : user_type
        param5 : first_name
        param6 : last_name
        param7 : email
        Responsible for user registration of all user types.
        SignUpForm is inheriting UserCreation form
    """
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    print("hgjgjh")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if user.is_student:
        	return redirect('sms:student_home')
        elif user.is_teacher:
        	return redirect('sms:teacher_home')
        elif user.is_parent:
            return redirect('sms:parent_home')

""" redirect to respective landing page"""
def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('sms:teacher_home')
        elif request.user.is_student:
            return redirect('sms:student_home')
        elif request.user.is_parent:
            return redirect('sms:parent_home')
    
    return render(request,'registration/login.html')


"""
    Homepage Views for all user types

"""
@method_decorator([login_required, student_required], name='dispatch')
class StudentHome(generic.ListView):
    """Home view for student """
    template_name = 'sms/student_home.html'

    def get_queryset(self):
        """Returns All attendances"""
        return Attendance.objects.all()

@method_decorator([login_required, teacher_required], name='dispatch')
class TeachertHome(generic.ListView):
    """ Home View for teacher"""
    template_name = 'sms/teacher_home.html'

    def get_queryset(self):
        """Return All Attendances"""
        return Attendance.objects.all()

@method_decorator([login_required, parent_required], name='dispatch')
class ParentHome(generic.ListView):
    """ Home View for Parent"""
    template_name = 'sms/parent_home.html'

    def get_queryset(self):
        """Return All Attendances"""
        return Attendance.objects.all()


"""
    Profile Update Views
    inheriting generic UpdateView
"""
@method_decorator([login_required, teacher_required], name='dispatch')
class TeacherProfileUpdateView(UpdateView):
	model = Teacher
	fields = ['first_name','last_name','email','gender','address','qualification']
	template_name_suffix = '_update_form'
	success_url = reverse_lazy('sms:teacher_home')

	def form_valid(self, form):
		return super(UpdateView,self).form_valid(form)

@method_decorator([login_required, parent_required], name='dispatch')
class ParentProfileUpdateView(UpdateView):
    model = Parent
    fields = ['first_name','last_name','email','gender','address']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('sms:parent_home')

    def form_valid(self, form):
        return super(UpdateView,self).form_valid(form)

@method_decorator([login_required, student_required], name='dispatch')
class StudentProfileUpdateView(UpdateView):
    model = Student
    fields = ['first_name','last_name','email','gender','address']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('sms:student_home')

    def form_valid(self, form):
        return super(UpdateView,self).form_valid(form)	 



"""
    attendance views for student parent and teacher
    inheriting generic ListView 
"""
@method_decorator([login_required, student_required], name='dispatch')
class AttendenceView(generic.ListView):
	model = Attendance
	template_name = 'sms/student_attendence_list.html'
	context_object_name = 'student_attendence_list'

	def get_queryset(self):
		"""Return the """
		return Attendance.objects.filter(student=self.request.user.student)

@method_decorator([login_required, teacher_required], name='dispatch')
class AttendenceAddView(CreateView):
	model = Attendance
	form_class = AddAttendenceForm

	template_name = 'sms/add_attendence.html'

	def form_valid(self, form):
		teacher = self.request.user.teacher
		attendance = form.save(commit=False)
		attendance.attendance_marked_by = teacher
		attendance.save()
		return redirect('sms:teacher_attn_view')

@method_decorator([login_required, teacher_required], name='dispatch')
class TeacherAttendenceView(generic.ListView):
	model = Attendance
	template_name = 'sms/student_attendence_list.html'
	context_object_name = 'student_attendence_list'
	def get_context_data(self, **kwargs):
		kwargs['is_teacher'] = True
		return super(generic.ListView,self).get_context_data(**kwargs)

	def get_queryset(self):
		"""Return the """
		return Attendance.objects.all()


@method_decorator([login_required, parent_required], name='dispatch')
class ParentAttendenceView(generic.ListView):
    model = Attendance
    template_name = 'sms/student_attendence_list.html'
    context_object_name = 'student_attendence_list'

    def get_queryset(self):
        """Return the """
        students = Student.objects.filter(parent=self.kwargs['parent_id'])
        return Attendance.objects.filter(student__in=students)


"""
    view for allocation of courses to students
"""
class AllocateCourseView(CreateView):
	model = StudentCourse
	fields = ('student', 'course' )
	template_name = 'sms/link_student_to_course.html'

	def form_valid(self, form):
		student_course = form.save(commit=False)
		student_course.save()
		return redirect('sms:course_allocation_list')

class AllocatedCoursesView(generic.ListView):
	model = StudentCourse
	template_name = 'sms/course_allocation_list.html'
	context_object_name = 'course_student_list'

	def get_context_data(self, **kwargs):
		kwargs['is_teacher'] = True
		return super(generic.ListView,self).get_context_data(**kwargs)

	def get_queryset(self):
		"""Return the """
		return StudentCourse.objects.all()


"""
    Views related to exams
    
"""
@method_decorator([login_required, parent_required], name='dispatch')
class StudentExamListView(generic.ListView):
	model = ExamResult
	template_name = 'sms/student_exam_list.html'
	context_object_name = 'student_exam_list'

	def get_queryset(self):
		"""Return the """
		students = Student.objects.filter(parent=self.kwargs['parent_id'])
		return ExamResult.objects.filter(student__in=students)

@method_decorator([login_required, teacher_required], name='dispatch')
class CreateExamView(CreateView):
    model = Exam
    fields = ('exam_name', 'description','subject', )
    template_name = 'sms/create_exam_form.html'

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.created_by = self.request.user
        exam.save()
        messages.success(self.request, 'The exam was created with success! Go ahead and add some questions now.')
        return redirect('sms:view_and_update_exam', exam.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamUpdateView(UpdateView):
    model = Exam
    context_object_name = 'exam'
    form_class = ExamForm
    template_name = 'sms/view_and_update_exam.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate()
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This view will only match the ids of existing exams that belongs
        to the logged in user.
        '''
        return self.request.user.exams.all()

    def get_success_url(self):
        return reverse('sms:view_and_update_exam', kwargs={'pk': self.object.pk})

@method_decorator([login_required, teacher_required], name='dispatch')
class ExamListView(ListView):
    model = Exam
    ordering = ('exam_name', )
    context_object_name = 'exams'
    template_name = 'sms/exam_list.html'

    def get_queryset(self):
        queryset = self.request.user.exams \
            .select_related('subject') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('exam_question_logs', distinct=True))
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamResultsView(ListView):
    model = ExamResult
    context_object_name = 'exams'
    template_name = 'sms/results.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        exams = self.request.user.exams.all()
        return ExamResult.objects.filter(exam__in=exams)


@login_required
@teacher_required
def add_question_to_exam(request, pk):
    # By filtering the exam by the url keyword argument `pk` and
    # by the created, which is the logged in user, we are protecting
    # exam will be able to add questions to it.
    exam = get_object_or_404(Exam, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('sms:view_and_update_exam', exam.pk)
    else:
        form = QuestionForm()

    return render(request, 'sms/add_question_to_exam.html', {'exam': exam, 'form': form})


@login_required
@teacher_required
def view_and_update_question(request, exam_pk, question_pk):
    # Simlar to the `question_add` view
    exam = get_object_or_404(Exam, pk=exam_pk, created_by=request.user)
    question = get_object_or_404(Question, pk=question_pk, exam=exam)

   
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('sms:view_and_update_exam', exam.pk)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'sms/view_and_update_question.html', {
        'exam': exam,
        'question': question,
        'form': form,
    })


@method_decorator([login_required, student_required], name='dispatch')
class StudentExamList(ListView):
    model = Exam
    ordering = ('name', )
    context_object_name = 'exams'
    template_name = 'sms/student_exam_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_courses = student.student_courses.values_list('course', flat=True)
        subjects = Subject.objects.filter(course__in=student_courses)
        taken_exams = student.exam_question_logs.values_list('pk', flat=True)
        queryset = Exam.objects.filter(subject__in=subjects) \
            .exclude(pk__in=taken_exams) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset



@method_decorator([login_required, student_required], name='dispatch')
class AppearedExamView(ListView):
    model = ExamLog
    context_object_name = 'taken_exams'
    template_name = 'sms/appeared_exam_list.html'
    

    def get_queryset(self):
        student = self.request.user.student
        queryset = student.exam_results \
            .select_related('exam', 'exam__subject') \
            .order_by('exam__exam_name')
        return queryset


@login_required
@student_required
def TakeExamView(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    student = request.user.student

    if student.exam_results.filter(student_id=student,exam_id=pk).exists():
        return redirect('sms:appeared_exam_list')
    data = request.POST.copy()
    total_questions = exam.questions.count()
    unanswered_questions = student.get_unanswered_questions(exam)
    total_unanswered_questions = unanswered_questions.count() or 0
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeExamForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                exam_log = form.save(commit=False)
                exam_log.student = student
                exam_log.exam = exam
                exam_log.question = question
                exam_log.save()
                if student.get_unanswered_questions(exam).exists():
                    return redirect('sms:take_exam', pk)
                else:
                    score = 0.0
                    ExamResult.objects.create(student=student, exam=exam,score=score)
                    messages.success(request, 'Congratulations! You completed the Exam %s with success!\
                     please wait while teacher evaluates.' % (exam.exam_name))
                    return redirect('sms:student_exam_list')
    else:
        form = TakeExamForm(question=question)

    return render(request, 'sms/take_exam.html', {
        'exam': exam,
        'question': question,
        'form': form,
        'progress': progress
    })

@login_required
@teacher_required
def EvaluateExamView(request, exam_res_id):
    exam_results = get_object_or_404(ExamResult, pk=exam_res_id)
    exam = exam_results.exam
    student = exam_results.student

    if student.exam_results.filter(student_id=student.pk,exam_id=exam.pk,evaluated=True).exists():
        return redirect('sms:exam_result_list')

    total_questions = exam.questions.count()
    unchecked_questions = student.exam_question_logs.filter(student_id=student.pk,exam_id=exam.pk,evaluated=False)
    total_unchecked_questions = unchecked_questions.count()
    progress = 100 - round(((total_unchecked_questions - 1) / total_questions) * 100)
    question = unchecked_questions.first()
    if request.method == 'POST':
        form = EvaluateExamForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                exam_log = ExamLog.objects.get(pk=question.pk)
                exam_log.score = form.cleaned_data.get("score")
                exam_log.evaluated = True
                exam_log.save()
                if student.get_unanswered_questions(exam).exists():
                    return redirect('sms:evaluate_exam', exam_res_id)
                else:
                    score = 0.0
                    exam_result = ExamResult.objects.get(student_id=student.pk, exam_id=exam.pk)
                    exam_result.evaluated = True
                    exam_result.score = ExamLog.objects.filter(student_id=student.pk,exam_id=exam.pk).aggregate(Sum('score'))['score__sum']
                    exam_result.save()
                    return redirect('sms:exam_result_list')
    else:
        form = EvaluateExamForm(question=question)

    return render(request, 'sms/evaluate_exam.html', {
        'exam': exam,
        'question': question,
        'form': form,
        'progress': progress
    })