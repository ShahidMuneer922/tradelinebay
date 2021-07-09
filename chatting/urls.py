from django.urls import path, include
from . import views





urlpatterns = [
    path('previous/<pk>/<id>/', views.previous_msg),  # THROUGH ID
    path('delete_message/<pk>/', views.delete_message),  # THROUGH ID
    path('disappear_message_start/<pk>/', views.disappear_message_start),  # THROUGH THREAD IN PK
    path('disappear_message/', views.disappear_messages),

]