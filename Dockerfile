FROM python:3.14.0rc1-slim-bullseye

# Install istioctl
ENV ISTIO_VERSION=1.27.0
ENV ISTIOCTL_DIR=/usr/local/bin

RUN apt-get update && apt-get install -y curl unzip ca-certificates && rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/istio/istio/releases/download/${ISTIO_VERSION}/istioctl-${ISTIO_VERSION}-linux-amd64.tar.gz \
    -o istioctl.tar.gz \
    && tar -xzf istioctl.tar.gz \
    && mv istioctl ${ISTIOCTL_DIR}/istioctl \
    && chmod +x ${ISTIOCTL_DIR}/istioctl \
    && rm istioctl.tar.gz

ENV PATH=$ISTIOCTL_DIR:$PATH

RUN useradd --create-home nonroot

WORKDIR /app

COPY istio_analyzer_exporter.py .

RUN pip install requests

USER nonroot

CMD ["python3", "istio_analyzer_exporter.py"]
