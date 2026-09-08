from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from colectas.filters import *
from colectas.recaptcha import PROJECT_ID, SITEKEY, create_assessment
from .models import *
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from django.conf import settings
from rest_framework.decorators import action
# Create your views here.

class CorporacionView(viewsets.ModelViewSet):
    serializer_class = CorporacionSerializer
    queryset = Corporacion.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CorporacionFilter
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='display')
    def display(self, request):
        queryset = self.get_queryset()
        serializer = CorporacionDisplaySerializer(queryset, many=True)
        return Response(serializer.data)

class Donador_CategoriaView(viewsets.ModelViewSet):
    serializer_class = Donador_CategoriaSerializer
    queryset = Donador_Categoria.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = Donador_CategoriaFilter
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='display')
    def display(self, request):
        queryset = self.get_queryset()
        serializer = Donador_CategoriaDisplaySerializer(queryset, many=True)
        return Response(serializer.data)

#@permission_classes([IsAuthenticated])
class EventoView(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    queryset = Evento.objects.all().order_by('-fecha_inicio')
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventoFilter
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='display')
    def display(self, request):
        queryset = self.get_queryset()
        serializer = EventoDisplaySerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='latest')
    def latest(self, request):
        queryset = self.filter_queryset( Evento.objects.order_by('-fecha_inicio') )[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DonadorView(viewsets.ModelViewSet):
    serializer_class = DonadorSerializer
    queryset = Donador.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DonadorFilter
    permission_classes = [IsAuthenticated]

class ClaseView(viewsets.ModelViewSet):
    serializer_class = ClaseSerializer
    queryset = Clase.objects.all()
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClaseFilter
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='display')
    def display(self, request):
        queryset = self.get_queryset()
        serializer = ClaseDisplaySerializer(queryset, many=True)
        return Response(serializer.data)

class UserioView(viewsets.ModelViewSet):
    serializer_class = UserioSerializer
    queryset = Userio.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserioFilter
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

#==========AUTENTICACION

# Register
class RegisterView(generics.CreateAPIView):
    queryset = Userio.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        
        user = self.request.data['username']
        self.request.data['rol'] = 'admin'
        if Userio.objects.filter(username=user).exists():
            return Response({'detail':'Este usuario ya existe', 'code':'duplicate_user'}, status=status.HTTP_417_EXPECTATION_FAILED)
        else:
            res = super().post(request, *args, **kwargs)
            return res

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request:request.HttpRequest):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'no hay token de refrees', 'code':'NO_REFRESH_TOKEN'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'error':'Token invalido'}, status=status.HTTP_400_BAD_REQUEST)
        response = Response({'detail':'Sesion cerrada'})
        response.delete_cookie('refresh_token')
        return response

class CookieLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print(str(request.data))
        token = request.data.get('grecaptchatoken')
        #if token:
            #assess = create_assessment(project_id=PROJECT_ID, recaptcha_key=SITEKEY, token=token, recaptcha_action='LOGIN')
            #print(assess)

        res = super().post(request, *args, **kwargs)
        if res.status_code == 200:
            refresh_token = res.data.pop('refresh')

            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=settings.COOKIE_SECURE,
                samesite=settings.COOKIE_SAMESITE,
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'], #7 dias
                path='/'
            )
            print('LOGIN: success for ' + str(request.data.get('username')))
            usr = Userio.objects.filter(username=request.data.get('username')).first()
            res.data['rol'] = usr.rol
            if usr.is_staff or usr.is_superuser: res.data['rol'] = 'admin'
        return res

class CookieRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('refresh_token')
        print('Cookie received:', token)
        if not token:
            print('no hay token')
            return Response({'detail': 'no hay token de refrees', 'code':'NO_REFRESH_TOKEN'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.data['refresh'] = token

        print('RESPONS: ', 'si')
        try:
            response = super().post(request, *args, **kwargs)
            
        except Exception as e:
            print('no jala el token: ', str(e))
            return Response({'detail':str(e), 'code':e.default_code}, status=status.HTTP_401_UNAUTHORIZED)
        
        if response.status_code == 200:
            new_refresh = response.data.pop('refresh', None)
            dec_token = RefreshToken(new_refresh)
            user_id = dec_token.get('user_id')
            usr = Userio.objects.filter(id=user_id).first()
            response.data['username'] = usr.username
            response.data['rol'] = usr.rol
            if usr.is_staff or usr.is_superuser: response.data['rol'] = 'admin'
            print('Recuperando sesion de: ' + usr.username)
            
            if new_refresh:
                response.set_cookie(
                    key='refresh_token',
                    value=new_refresh,
                    httponly=True,
                    secure=settings.COOKIE_SECURE,
                    samesite=settings.COOKIE_SAMESITE,
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'], #7 dias
                    path='/',
                )
        return response

        