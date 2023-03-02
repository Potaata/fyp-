from django.urls import path
from .views import HomePageView
from accounts import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
