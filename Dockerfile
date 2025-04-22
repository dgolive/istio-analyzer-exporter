FROM python:3.13-slim

# Install istioctl
ENV ISTIO_VERSION=1.26.0-beta.0
ENV ISTIOCTL_DIR=/usr/local/bin

RUN apt-get update && apt-get install -y curl unzip ca-certificates && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://istio.io/downloadIstioctl | ISTIO_VERSION=$ISTIO_VERSION sh - \
    && mv ~/.istioctl/bin/istioctl $ISTIOCTL_DIR \
    && chmod +x $ISTIOCTL_DIR/istioctl

ENV PATH=$ISTIOCTL_DIR:$PATH

WORKDIR /app

COPY istio_analyzer_exporter.py .

RUN pip install requests

CMD ["python3", "istio_analyzer_exporter.py"]
