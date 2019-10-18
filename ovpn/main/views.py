from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
import os
from openvpn_utils.OpenVPN import OpenVPN
from django.contrib.admin.views.decorators import staff_member_required
from main.forms import OvpnConfigForm
from django.views.generic.edit import FormView

@staff_member_required(login_url='/accounts/login/')
def ovpn_edit(request):
    ovpn = OpenVPN()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OvpnConfigForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            config=form.cleaned_data['config']
            ovpn.save_server_config_file(config)
            # redirect to a new URL:
            return HttpResponseRedirect('/main')

    # if a GET (or any other method) we'll create a blank form
    else:
        config = ovpn.get_server_config_file()
        if config is None:
            config = 'Cannot get OpenVPN server configuration!!!!'
        form = OvpnConfigForm(initial={'config': config})
        return render(request, 'ovpn_edit.html', {'form': form})


@login_required(login_url='/accounts/login/')
def index(request):
    current_user = str(request.user)
    ovpn = OpenVPN()
    if ovpn.is_config_file_exists(current_user)==False:
        ovpn.create_user_certificate(current_user)
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
