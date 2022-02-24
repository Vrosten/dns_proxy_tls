FROM python:latest

WORKDIR /app/dns_proxy
COPY . /app/dns_proxy
RUN sudo apt update 
RUN sudo apt-get install python3-pip -y
CMD ["python","main.py","&"]