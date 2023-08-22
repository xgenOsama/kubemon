Docker Desktop and Kubernetes must be up and running, Kubernetes must be in a clean state. Helm must be installed; check it with
```
helm version
```
If helm isn't there, just use homebrew:
```
brew install helm
```
Add the repo and install it:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```
Check status then:
```
kubectl --namespace default get pods -l "release=prometheus"
kubectl port-forward svc/prometheus-grafana 8040:80
kubectl get secret prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; 
prom-operator
```

**HINT: If you facing any issues with prometheus-node-exporter, do the following steps:**
- Uninstall the release:
    ```
    helm uninstall prometheus
    ```
- Re-install with:
    ```
    helm install prometheus prometheus-community/kube-prometheus-stack --set prometheus-node-exporter.hostRootFsMount=false
    ```

```