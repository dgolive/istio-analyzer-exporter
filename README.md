# Istio Analyzer Exporter

## About
Istio-Analyzer-Exporter helps to ensure that the Istio Service Mesh is configured correctly by providing analytics collected to a logging management tool and then can be presented in a Grafana dashboard.

## How does it work?
Istio-Analyzer-Exporter tool collects, processs and forward logs to a logging management tool. The version v1.0.0 uses Grafana Loki as logging management tool.

Istio-Analyzer-Exporter works with "istioctl" who is a configuration command line utility that allows service operators to debug and diagnose their Istio service mesh deployments.


### Istio Analyzer Dashboard  

![alt text](image.png)


## How to deploy
````
kubectl apply -f istio-analyzer-exporter.yaml
```


### References:
https://istio.io/latest/docs/reference/commands/istioctl/  
https://istio.io/latest/docs/reference/commands/istioctl/#istioctl-analyze  
https://istio.io/latest/docs/ops/diagnostic-tools/istioctl/  



### CONTRIBUTORS
```
 2058  sudo docker build -t danilogo/istio-analyzer-exporter:v1.0.0 .
 2063  sudo docker login -u danilogo
 2064  sudo docker push danilogo/istio-analyzer-exporter:v1.0.0 

```

#### ERROR/WARNING SAMPLES
errors found it to fix
Error [IST0161] (Gateway aks-istio-ingress/backstage-gw) The credential referenced by the Gateway backstage-gw in namespace aks-istio-ingress is invalid, which can cause the traffic not to work as expected.

Warning [IST0138] (Gateway aks-istio-ingress/aks-sre-nonprod-gateway-mfe) Duplicate certificate in multiple gateways [aks-istio-ingress/aks-sre-nonprod-gateway-mfe aks-istio-ingress/alloy-nonprod-gw] may cause 404s if clients re-use HTTP2 connections.