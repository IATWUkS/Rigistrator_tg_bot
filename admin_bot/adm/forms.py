from django import forms

from .models import pre_registration_data, Organization, Admin_profile


class Reg_form(forms.ModelForm):
    class Meta:
        model = pre_registration_data
        fields = ('id_tg', 'name', 'surname', 'email', 'company', 'position', 'number', 'data_processing', 'status_user', 'login_bitrix', 'password_bitrix')
        widgets = {
            'name': forms.TextInput,
            'surname': forms.TextInput,
            'email': forms.TextInput,
            'company': forms.TextInput,
            'position': forms.TextInput,
            'number': forms.TextInput,
            'data_processing': forms.TextInput,
            'status_user': forms.TextInput,
            'login_bitrix': forms.TextInput,
            'password_bitrix': forms.TextInput,
        }


class Organization_form(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name', 'INN', 'KPP', 'OGRN', 'adress', 'Mailing_address', 'FIO_director', 'email', 'id_tg', 'number')
        widgets = {
            'name': forms.TextInput,
            'INN': forms.TextInput,
            'KPP': forms.TextInput,
            'OGRN': forms.TextInput,
            'adress': forms.TextInput,
            'Mailing_address': forms.TextInput,
            'FIO_director': forms.TextInput,
            'email': forms.TextInput,
            'id_tg': forms.TextInput,
            'number': forms.TextInput,
        }


class Admin_form(forms.ModelForm):
    class Meta:
        model = Admin_profile
        fields = ('id_tg', 'FIO', 'company', 'rang')
        widgets = {
            'id_tg': forms.TextInput,
            'FIO': forms.TextInput,
            'rang': forms.TextInput,
        }