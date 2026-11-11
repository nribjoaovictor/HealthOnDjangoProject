from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from login import views as login_views
from usuarios import views as usuarios_views

urlpatterns = [


    path('', login_views.login_view, name='login'),
    path('login/', include('login.urls')),

    path('medico/', usuarios_views.dashboard_medico, name='dashboard_medico'),
    path('paciente/', usuarios_views.dashboard_paciente, name='dashboard_paciente'),
    path('farmacia/', usuarios_views.dashboard_farmacia, name='dashboard_farmacia'),

    path('medico/', include('usuarios.urls')),
]
if not settings.READ_ONLY_DEMO:
    urlpatterns.append(path("admin/", admin.site.urls))
