from django.urls import path
from . import views


app_name = 'classes'
urlpatterns = [
    path("", views.index, name="index"),
    path("create_class", views.create_class, name="create_class"),
    path("manage_class/<int:pk>/", views.manage_class, name="manage_class"),
    path("enroll/<int:pk>", views.enroll, name="enroll"),
    path("last_check/<int:pk>", views.last_check, name="last_check"),
    path("continue_learning/<int:pk>", views.continue_learning, name="continue_learning"),
    path("take_quiz/<int:pk>", views.take_quiz, name="take_quiz"),
    path("submit_quiz/<int:pk>", views.submit_quiz, name="submit_quiz"),
    path("log_out/", views.log_out, name="log_out"),
    path("profile_settings/<int:pk>", views.profile_settings, name="profile_settings"),
    path("manage/<int:class_pk>/dismiss/<int:user_pk>/", views.dismiss, name="dismiss"),
]