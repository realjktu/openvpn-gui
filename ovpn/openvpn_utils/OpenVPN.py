from django.http import HttpResponse
import os, subprocess

class OpenVPN:
    def get_config_file_response(self, username):
        user_config = self.get_user_config(username)
        if user_config is not None:
            response = HttpResponse(user_config, content_type="text/plain")
            response['Content-Disposition'] = 'inline; filename=' + username+'.ovpn'
            return response
        return None

    def is_config_file_exists(self, username):
        user_config = self.get_user_config(username)
        if user_config is not None:
            return True
        return False

    def get_user_config(self, username):
        output = ''
        try:
            bashCommand = ("/ovpn_getclient %s"%(username))
#            bashCommand = ("echo %s config"%(username))
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if process.returncode != 0:
                return None
        except:
            return None
        return output

    def create_user_certificate(self, username):
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

