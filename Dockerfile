FROM python:latest

WORKDIR /app/dns_proxy
COPY . /app/dns_proxy
RUN pip install netifaces 
CMD ["python","main.py","&"]
#CMD ["python","netint.py"]                          