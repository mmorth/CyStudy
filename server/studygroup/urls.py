from django.urls import path
from studygroup import views

app_name = 'studygroup'
urlpatterns = [
    # Studygroup CRUD
    path('<slug:username>/group/create/', views.create_study_group, name='create_study_group'),
    path('<int:id>/remove/', views.remove_study_group, name='remove_study_group'),
    path('<int:studygroup_id>/update/', views.update_study_group, name='update_study_group'),

    # Join / leave study group
    path('join/', views.join_study_group, name='join_study_group'),
    path('<int:studygroup_id>/leave/', views.leave_study_group, name='leave_study_group'),

    # Display studygroup / course information
    path('show/<int:user_id>/<int:studygroup_id>/', views.show_study_group, name='show_study_group'),
    path('show/course/<int:course_id>/', views.show_course, name='show_course'),
    path('list/', views.study_group_list, name='study_group_list'),
    path('student/<slug:username>/studygroups/', views.student_study_group, name='student_study_group'),
    path('courses/list/', views.course_list, name='course_list'),
    path('student/<slug:username>/studygroups/notmember/', views.study_group_not_member, name='study_group_not_member'),

    # Course CRUD
    path('course/create/', views.create_course, name='create_course'),
    path('course/<int:course_id>/remove/', views.remove_course, name='remove_course'),
    path('course/<int:course_id>/update/', views.update_course, name='update_course'),
    #TODO retrieve
]
