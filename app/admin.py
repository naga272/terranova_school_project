from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from app.models import (
    Progetto, Teams, BaseDataUser,
    Ruoli, Messaggio, Periodi,
    Ferie, NormalUser
)


@admin.register(BaseDataUser)
class BaseDataUserAdmin(UserAdmin):
    pass


admin.site.register(Progetto)
admin.site.register(Teams)
# admin.site.register(BaseDataUser)
admin.site.register(NormalUser)
admin.site.register(Messaggio)
admin.site.register(Ruoli)
admin.site.register(Periodi)
admin.site.register(Ferie)
