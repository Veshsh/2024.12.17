from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
admin.site.unregister(Group)
from .models import * 
class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('login',)
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2: raise forms.ValidationError("Passwords do not match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit: user.save()
        return user
class UpdateUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('password', 'login' ,'is_active','is_staff','is_superuser','is_observer','history_save','history','date_joined',)
    def clean_password(self):
        return self.initial["password"]
class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm
    list_display = ('login', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = ((None, {'fields': ('login', 'password')}),('Permissions', {'fields': ('is_active', 'is_staff','is_superuser','is_observer','history_save','history','date_joined')}),)
    add_fieldsets = ((None,{'classes': ('wide',),'fields': ('login', 'password1','password2')}),)
    search_fields = ('login',)
    ordering = ('login',)
    filter_horizontal = ()
admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Log)
class MachinAdmin(admin.ModelAdmin):
    form =MachinForm
admin.site.register(Machin,MachinAdmin )
admin.site.register(Machin_Group)
admin.site.register(Machine_request_one_comand)




