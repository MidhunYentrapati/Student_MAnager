# student_manager/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('home/', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    path('attendance/',include('attendance.urls')),
    path('', accounts_views.redirect_to_about, name='redirect_to_about'),
    path('todo/', include('todo.urls')),
]
