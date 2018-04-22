from django.urls import path

from data import views

app_name = 'data'
urlpatterns = [
    path('options/', views.options, name='options'),

    # Login and logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Change account information
    path('account/create/', views.create_user, name='create_account'),
    path('account/<int:id>/delete/', views.delete_user, name='delete_user'),
    path('account/<int:user_id>/settings/', views.change_user_settings, name='change_user_settings'),

    # Display information about users
    path('user/<slug:username>/home/', views.show_home, name='show_home'),
    path('user/<int:id>/display/', views.display_user, name='display_user'),
    path('user/list/', views.list_users, name='list_users'),

    # Report user
    path('user/<int:id>/report/', views.report_user, name='report_user'),
]