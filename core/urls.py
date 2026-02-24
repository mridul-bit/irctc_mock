"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from app.views import (
    RegisterView, LoginView, TrainView, TrainSearchView, 
    BookingView, MyBookingsView, AnalyticsTopRoutesView,SystemLogsView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='ui'),
    
    
    path('api/system/logs/', SystemLogsView.as_view(), name='system_logs'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/trains/', TrainView.as_view(), name='add_train'),
    path('api/trains/search/', TrainSearchView.as_view(), name='search_trains'),
    path('api/bookings/', BookingView.as_view(), name='book_seat'),
    path('api/bookings/my/', MyBookingsView.as_view(), name='my_bookings'),
    path('api/analytics/top-routes/', AnalyticsTopRoutesView.as_view(), name='top_routes'),
]

