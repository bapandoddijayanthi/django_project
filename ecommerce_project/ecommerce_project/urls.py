
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')), # Include URLs from your 'shop' app
    # Include Django's built-in authentication URLs
    # This provides URLs like /accounts/login/, /accounts/logout/, /accounts/password_change/, etc.
    path('accounts/', include('django.contrib.auth.urls')),
    # We'll add a custom registration view later, but for now, we'll use the admin to create users.
]

# Serve media files during development (IMPORTANT: Do NOT use in production)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

