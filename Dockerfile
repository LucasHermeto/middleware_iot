FROM python:3.7-alpine

ENV BROKER_IP="${BROKER_IP:-"localhost"}" \
    INFLUX_IP="${INFLUX_IP:-"localhost"}"

RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY heimdall.py heimdall.py
CMD ["python", "heimdall.py"]