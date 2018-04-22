from django.urls import path
from notes import views

app_name = 'notes'
urlpatterns = [
    path('<int:studygroup_id>/create/', views.create_note),
    path('<int:note_id>/delete/', views.delete_note),
    path('<int:studygroup_id>/<int:note_id>/edit/', views.edit_note),
    path('<int:studygroup_id>/', views.get_notes),
]
