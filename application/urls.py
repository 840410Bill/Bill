from django.urls import path

from . import views
app_name = "application"
urlpatterns = [
    path('origin_url/', views.origin_url, name='origin_url'),
    path('r/<str:short_code>/', views.redirect_to_original_url, name='redirect_to_original_url'),
]