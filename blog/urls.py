from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('create_post/', views.create_post, name='create_post'),
    path('ajax_create_post/', views.ajax_create_post, name='ajax_create_post'),
    path('edit_post/<pk>/', views.edit_post, name='edit_post'),
    path('ajax_edit_post/<pk>/', views.ajax_edit_post, name='ajax_edit_post'),
    path('ajax_delete_post/<pk>/', views.ajax_delete_post, name='ajax_delete_post'),
]

