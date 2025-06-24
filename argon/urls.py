from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.dashboard import views
from django.conf import settings
from apps.tasks import views as task_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('tables/', views.tables, name='tables'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/<int:profile_id>/', views.edit_profile, name='edit_profile'),
    path('edit_user/<int:profile_id>/', views.edit_user, name='edit_user'),
    path('delete_profile/<int:profile_id>/', views.delete_profile, name='delete_profile'),
    path('sign-in/', views.sign_in, name='signin'),
    path('sign-up/', views.sign_up, name='signup'),
    path('export/', views.export_data, name='export_data'),
    path('export_bitacora/', views.export_data_bitacora, name='export_data_bitacora'),
    path('close/', views.close, name='close'),

    # URLs de la app tasks
    path('tasks/', task_views.tasks, name='tasks'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
