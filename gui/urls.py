from django.urls import path
from . import views

urlgui = [
    path("", views.SingIn, name="url-singin"),
    path("logout/", views.Logout, name="url-logout"),
    path("list", views.List, name="url-list"),
    path("list/<int:id>", views.List, name="url-list"),
    path("connect/ssh/<int:id>/", views.connect_ssh, name="url-connect-ssh"),
]
