from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


def trigger_error(request):
    division_by_zero = 1 / 0



urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('users/', include('users.urls', namespace='users')),
    path('ticket/', include('ticket.urls', namespace='ticket')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('accounting/', include('accounting.urls', namespace='accounting')),
    path('workreport/', include('workreport.urls', namespace='workreport')),
    path('task/', include('task.urls', namespace='task')),
    path('timesheet/', include('timesheet.urls', namespace='timesheet')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('sentry-debug/', trigger_error),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)