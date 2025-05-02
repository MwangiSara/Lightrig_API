from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from bookings.views import BookingViewSet,ClientViewset,ContactViewSet
from accounts.views import PhotographerViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('clients', ClientViewset, basename='clients'),
router.register('bookings', BookingViewSet, basename='bookings'),
router.register('contact', ContactViewSet, basename='contact'),
router.register('photographer',PhotographerViewSet, basename='photographer')



urlpatterns = [
    path('', lambda request: redirect('api/')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)