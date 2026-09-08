from django.contrib import admin
from .models import Donador_Categoria
from django.contrib.auth.admin import UserAdmin
from .models import Userio
# Register your models here.
admin.site.register(Donador_Categoria)
admin.site.register(Userio, UserAdmin)