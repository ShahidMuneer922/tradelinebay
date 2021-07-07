from django.urls import path, include
from . import views





urlpatterns = [
    path('previous/<pk>/<id>/', views.previous_msg),  # THROUGH ID

]