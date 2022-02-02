FROM ubuntu: latest

WORKDIR /app/udp_tcp_totls
COPY . /app/udp_tcp_totls/
RUN apt-get -y update && apt-get install -y python3
CMD ["python3","main.py"]