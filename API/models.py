from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from datetime import timedelta, datetime
from netfields import InetAddressField, NetManager
from django import forms
class UserManager(BaseUserManager):
    def create_user(self, login, history_save=True, password=None,commit=True):
        if not login: raise ValueError(_('Users must have a login'))
        user = self.model(login=login,history_save=history_save)
        user.set_password(password)
        if commit: user.save(using=self._db)
        return user
    def create_superuser(self, login, password):
        user = self.create_user(password=password,login=login,commit=False)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(_('login'), max_length=150, blank=True,unique=True)
    is_active = models.BooleanField(_('active'),default=True,help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),)
    is_staff = models.BooleanField(_('staff status'),default=False,help_text=_('Designates whether the user can log into this admin site.'),)
    is_observer = models.BooleanField(default=False)
    history_save = models.BooleanField(default=True)
    history =models.FileField()
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'login'
    def get_full_name(self):
        return self.login
    def __str__(self):
        return self.login
class Group(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=512)
class Machin(models.Model):
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    user=models.ForeignKey(User, on_delete=models.PROTECT)
    group=models.ForeignKey(Group, on_delete=models.PROTECT)
    history_save = models.BooleanField(default=True)
    log_save = models.BooleanField(default=True)
    ip = InetAddressField()
    port=models.IntegerField(validators=[MaxValueValidator(65535),MinValueValidator(1)])
    objects = NetManager()
    user_monitor_permision=models.BooleanField(default=True)
    user_user_permision=models.BooleanField(default=True)
    group_monitor_permision=models.BooleanField(default=True)
    group_user_permision=models.BooleanField(default=True)
    other_monitor_permision=models.BooleanField(default=True)
    other_user_permision=models.BooleanField(default=True)
    def form(self):
        return MachinForm(instance=self)
    def getip(self):
        ip=str(self.ip.ip)
        return ip
class MachinForm(forms.ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput(), required = False)
    group=None
    try:
        group = forms.Select(choices=Group.objects.all().values_list('id', 'name'))
    except:
        group=None
    class Meta:
        model = Machin
        fields = ('__all__')
class Log(models.Model):
    machin =models.ForeignKey(Machin, on_delete=models.CASCADE)
    time_save=models.DateTimeField(auto_now_add=True)
    log =models.FileField(editable=False,auto_created = True)
    history =models.FileField(editable=False,auto_created = True)
class Machin_Group(models.Model):
    machin = models.ManyToManyField(Machin,related_name='machin_group')
    name = models.CharField(max_length=64, unique=True)
class Machine_request_one_comand(models.Model):
    machin_group=models.ForeignKey(Machin_Group, on_delete=models.CASCADE)
    machin=models.ForeignKey(Machin, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    color = ColorField()
    request_file_path=models.FileField(editable=False)
