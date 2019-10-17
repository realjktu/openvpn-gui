#FROM python:3.8.0-alpine3.10
FROM alpine:3.10
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing/" >> /etc/apk/repositories && \
    apk add --update openvpn iptables bash easy-rsa openvpn-auth-pam google-authenticator pamtester nginx uwsgi-python3 py3-pip && \
    ln -s /usr/share/easy-rsa/easyrsa /usr/local/bin && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /var/cache/distfiles/*
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt
# Needed by scripts
ENV OPENVPN /etc/openvpn
ENV EASYRSA /usr/share/easy-rsa
ENV EASYRSA_PKI $OPENVPN/pki
ENV EASYRSA_VARS_FILE $OPENVPN/vars

# Prevents refused client connection because of an expired CRL
ENV EASYRSA_CRL_DAYS 3650

COPY ovpn_getclient /
COPY ovpn_uwsgi.ini /
COPY nginx.conf /etc/nginx/nginx.conf
COPY ovpn/. /ovpn/
WORKDIR /ovpn
RUN mkdir -p /var/tmp/nginx/
EXPOSE 80/tcp
CMD nginx && python3 manage.py migrate && uwsgi --ini /ovpn_uwsgi.ini
