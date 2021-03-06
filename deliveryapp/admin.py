from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from .models import *
# Register your models here.

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('email',)
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Customer
        fields = ('email', 'name','surname','birthday','phone_number','address', 'is_staff', 'is_active', 'is_superuser')
    def clean_password(self):

        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm


    list_display = ('email', 'name', 'surname', 'birthday', 'phone_number', 'address', 'registration_date')
    list_filter = ('is_staff','email', 'birthday', 'registration_date')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','surname','address','phone_number', 'birthday')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'address', 'birthday', 'password1', 'password2'),
        }),
    )
    search_fields = ('is_staff','email', 'birthday', 'registration_date',)
    ordering = ('is_staff','email', 'birthday', 'registration_date',)
    filter_horizontal = ()

      
admin.site.register(Customer,UserAdmin)
admin.site.unregister(Group)
admin.site.register(FAQ)
admin.site.register(Order)
admin.site.register(Partner)
admin.site.register(Storage)