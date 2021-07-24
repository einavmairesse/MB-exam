from django.urls import path

from . import views

urlpatterns = [
    path('', views.instances_page),
    path('create/', views.create_instances_view),
    path('start/', views.start_test_page),
    path('running_tests/', views.running_tests_page),
    path('stop/', views.stop),
    path('update/', views.update)
]