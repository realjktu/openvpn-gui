from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download_ovpn', views.download_ovpn, name='download_ovpn'),
    path('ovpn_edit', views.ovpn_edit, name='ovpn_edit'),
    path('accounts/', include('django.contrib.auth.urls')),
#    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
