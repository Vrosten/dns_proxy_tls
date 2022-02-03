FROM python:latest

WORKDIR /app/dns_proxy
COPY . /app/dns_proxy
RUN ["python3","main.py -i 192.168.0.21 -p 53"]