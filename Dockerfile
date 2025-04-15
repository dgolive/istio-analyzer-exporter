FROM python:3.9-slim

WORKDIR /app

COPY istio_loki_exporter.py .

RUN pip install requests

CMD ["python", "istio_loki_exporter.py"]