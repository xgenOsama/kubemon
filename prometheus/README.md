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
    kubectl patch ds prometheus-prometheus-node-exporter --type "json" -p '[{"op": "remove", "path" : "/spec/template/spec/containers/0/volumeMounts/2/mountPropagation"}]'
    ```

```


```
helm search hub Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus
kubectl patch ds prometheus-prometheus-node-exporter --type "json" -p '[{"op": "remove", "path" : "/spec/template/spec/containers/0/volumeMounts/2/mountPropagation"}]'
kubectl get service
kubectl port-forward svc/prometheus-server 9090:80
helm search hub grafana
helm repo add grafana https://grafana.github.io/helm-charts 
helm repo update
helm install grafana grafana/grafana
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
kubectl get service
kubectl port-forward svc/grafana 8080:80
kubectl apply -f ./
helm upgrade prometheus prometheus-community/prometheus --set server.persistentVolume.enabled=true --set server.persistentVolume.storageClass=local-storage --set server.persistentVolume.existingClaim=prometheus-pvc 
helm upgrade grafana grafana/grafana --set persistence.enabled=true,persistence.storageClassName="local-storage",persistence.existingClaim="grafana-pvc" 



```