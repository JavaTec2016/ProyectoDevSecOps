from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'corporaciones', CorporacionView, 'corporaciones')
router.register(r'categorias', Donador_CategoriaView, 'categorias')
router.register(r'eventos', EventoView, 'eventos')
router.register(r'donadores', DonadorView, 'donadores')
router.register(r'clases', ClaseView, 'clases')
router.register(r'usuarios', UserioView, 'usuarios')
urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/login/", CookieLoginView.as_view(), name='login'),
    path("api/v1/auth/refresh/", CookieRefreshView.as_view(), name='refresh'),
    path("api/v1/auth/registrar/", RegisterView.as_view(), name='registrar'),
    path("api/v1/auth/logout/", LogoutView.as_view(), name='logout'),
    path("schema/", SpectacularAPIView.as_view(), name='schema'),
    path("docs/", SpectacularSwaggerView.as_view(), name='docs'),
]
