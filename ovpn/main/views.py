from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, Http404
import os
from openvpn_utils.OpenVPN import OpenVPN

@login_required(login_url='/accounts/login/')
def index(request):
    current_user = str(request.user)
    ovpn = OpenVPN()
    is_config_exists = False
    if ovpn.is_config_file_exists(current_user):
        is_config_exists = True
    context = {'is_config_exists': is_config_exists}
    return render(request, 'index.html', context)

@login_required(login_url='/accounts/login/')
def download_ovpn(request):
    current_user = str(request.user)
    ovpn = OpenVPN()
    if ovpn.is_config_file_exists(current_user):
        return ovpn.get_config_file_response(current_user)
    else:
        raise Http404
