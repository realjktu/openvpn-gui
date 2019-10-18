from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User as usr
from openvpn_utils.OpenVPN import OpenVPN
import subprocess, os

def create_customer(sender, instance, created, **kwargs):
    client_name = instance
    print("Save is called for user %s"%client_name)
    user_exists = True
    try:
      u = usr.objects.get(username=client_name)
    except User.DoesNotExist:
        print("User does not exist")
        user_exists = False
    if user_exists is False:
      ovpn = OpenVPN()
      ovpn.create_user_certificate(client_name)
      '''
      bashCommand = ("easyrsa build-client-full %s nopass"%client_name)
      print(bashCommand)
      process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
      while True:
        line = process.stdout.readline()
        if line != b'':
          print(line.rstrip())
        else:
          break
      output, error = process.communicate()
      '''
      '''
      bashCommand = ("/ovpn_getclient %s"%client_name)
      process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
      while True:
        line = process.stdout.readline()
        if line != b'':
          print(line.rstrip())
        else:
          break
      output, error = process.communicate()
      '''
    #easyrsa build-client-full {client_name} nopass;
    #/ovpn_getclient {client_name} > certificate.ovpn;    

def delete_customer(sender, instance, **kwargs):
    client_name = instance
    print("Delete is called for %s user"%client_name)
    ovpn = OpenVPN()
    ovpn.delete_user_certificate(client_name)


#class User(models.Model):
#    user_name = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')

#signals.post_save.connect(receiver=create_customer, sender=usr, dispatch_uid="create_customer")
signals.post_delete.connect(receiver=delete_customer, sender=usr, dispatch_uid="create_customer")

