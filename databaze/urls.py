from django.urls import path, include
from . import views
from . import url_handlers

urlpatterns = [
    path("klient_index/", views.KlientIndex.as_view(), name = "klient_index"),
    path("<int:pk>/klient_kontakt/", views.KontaktIndex.as_view(), name = "klient_kontakt"),
    path("<int:pk>/klient_detail/", views.DetailKlientView.as_view(), name="klient_detail"),
    path("create_klient/", views.CreateKlient.as_view(), name="create_klient"),
    path("create_kontakt/", views.CreateKontakt.as_view(), name="create_kontakt"),
    path("<int:pk>/edit/", views.EditKlient.as_view(), name="edit_klient"),
    path("register/", views.UzivatelViewRegister.as_view(), name = "registrace"),
    path("login/", views.UzivatelViewLogin.as_view(), name = "login"),
    path("logout/", views.logout_user, name = "logout"),
    path("", url_handlers.index_handler),
]