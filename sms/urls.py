from django.conf.urls import url

from . import views

app_name = 'sms'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^student/$', views.StudentHome.as_view(), name='student_home'),
    url(r'^student/exam/list/$', views.StudentExamList.as_view(), name='student_exam_list'),
    url(r'^student/exam/(?P<pk>[0-9]+)/take/$', views.TakeExamView, name='take_exam'),
    url(r'^student/exam/appeared/$', views.AppearedExamView.as_view(), name='appeared_exam_list'),
    url(r'^student/profileupdate/(?P<pk>[0-9]+)/$', views.StudentProfileUpdateView.as_view(), name='edit_student_profile'),    
    url(r'^teacher/$', views.TeachertHome.as_view(), name='teacher_home'),
    url(r'^teacher/profileupdate/(?P<pk>[0-9]+)/$', views.TeacherProfileUpdateView.as_view(), name='edit_teacher_profile'),
    url(r'^teacher/attendence/add/$', views.AttendenceAddView.as_view(), name='add_attendence'),
    url(r'^teacher/attendence/view/$', views.TeacherAttendenceView.as_view(), name='teacher_attn_view'),
    url(r'^teacher/linkcourse/add/$', views.AllocateCourseView.as_view(), name='link_course'),
    url(r'^teacher/linkcourse/list/$', views.AllocatedCoursesView.as_view(), name='course_allocation_list'),
    url(r'^teacher/linkcourse/list/$', views.AllocatedCoursesView.as_view(), name='course_allocation_list'),
    url(r'^teacher/exam/list/$', views.ExamListView.as_view(), name='exam_list'),
    url(r'^teacher/exam/create/$', views.CreateExamView.as_view(), name='create_exam'),
    url(r'^teacher/exam/view/(?P<pk>[0-9]+)/$', views.ExamUpdateView.as_view(), name='view_and_update_exam'),
    url(r'^teacher/exam/results/$', views.ExamResultsView.as_view(), name='exam_result_list'),
    url(r'^teacher/exam/(?P<exam_res_id>[0-9]+)/evaluate$', views.EvaluateExamView, name='evaluate_exam'),
    url(r'^teacher/exam/(?P<pk>[0-9]+)/question/create/$', views.add_question_to_exam, name='add_question_to_exam'),
    url(r'^teacher/exam/(?P<exam_pk>[0-9]+)/question/(?P<question_pk>[0-9]+)/view/$', views.view_and_update_question, name='view_and_update_question'),
    url(r'^student/attendence/(?P<student_id>[0-9]+)/$', views.AttendenceView.as_view(), name='student_attendence_list'),
    url(r'^parent/$', views.ParentHome.as_view(), name='parent_home'),
    url(r'^parent/profileupdate/(?P<pk>[0-9]+)/$', views.ParentProfileUpdateView.as_view(), name='edit_parent_profile'),    
    url(r'^parent/(?P<parent_id>[0-9]+)/parent_attn/$', views.ParentAttendenceView.as_view(), name='student_attn_for_parent_list'),
    url(r'^parent/exam/(?P<parent_id>[0-9]+)/$', views.StudentExamListView.as_view(), name='student_exams_for_parent_list')
]