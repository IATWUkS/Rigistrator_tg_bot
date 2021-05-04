from django.contrib import admin
from .models import pre_registration_data, Organization, Admin_profile
from .forms import Reg_form, Organization_form, Admin_form


@admin.register(pre_registration_data)
class Pre_reg_data(admin.ModelAdmin):
    list_display = ('id_tg', 'name', 'surname', 'email', 'status_user')
    form = Reg_form


@admin.register(Organization)
class Organiz_model(admin.ModelAdmin):
    list_display = ('name', 'FIO_director', 'id_tg', 'email', 'number')
    form = Organization_form


@admin.register(Admin_profile)
class Admin_profile_model(admin.ModelAdmin):
    list_display = ('id_tg', 'FIO', 'company')
    form = Admin_form
