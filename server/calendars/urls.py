from django.urls import path

from calendars import views

app_name = 'calendars'
urlpatterns = [
    path('<int:studygroup_id>/meeting/', views.create_group_meeting, name='create_group_meeting'),
    path('<int:studygroup_id>/meeting/<int:meeting_id>/', views.edit_group_meeting, name='edit_group_meeting'),
    path('<int:studygroup_id>/meeting/<int:meeting_id>/delete/', views.delete_group_meeting, name='delete_group_meeting'),
    path('<int:studygroup_id>/meeting/<int:meeting_id>/details/', views.show_group_meeting, name='show_group_meeting'),
    path('<int:studygroup_id>/meetings/list/', views.list_group_meetings, name='list_group_meetings'),
]