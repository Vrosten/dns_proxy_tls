FROM python:latest

WORKDIR /app/dns_proxy
COPY . /app/dns_proxy
CMD ["python","main.py","&"]