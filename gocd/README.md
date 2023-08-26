# Add the GoCD helm chart repository:
```shell
helm repo add gocd https://gocd.github.io/helm-chart
helm repo update
helm install gocd gocd/gocd --namespace gocd --create-namespace
### output 
NAME: gocd
LAST DEPLOYED: Sun Aug 27 01:23:22 2023
NAMESPACE: gocd
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
1. Get the GoCD server URL by running these commands:
    It may take a few minutes before the IP is available to access the GoCD server.
         echo "GoCD server public IP: http://$(kubectl get ingress gocd-server --namespace=gocd  -o jsonpath='{.status.loadBalancer.ingress[0].ip}')"

2. Get the service account token to configure the elastic agent plugin by doing the following:
    A default role gocd with cluster scoped privileges has been configured.
    
    The service account called gocd in namespace gocd has been associated with the role. To check,
        secret_name=$(kubectl get serviceaccount gocd --namespace=gocd  -o jsonpath="{.secrets[0].name}")
        kubectl get secret $secret_name --namespace=gocd -o jsonpath="{.data['token']}" | base64 --decode

    To obtain the CA certificate, do
        kubectl get secret $secret_name --namespace=gocd  -o jsonpath="{.data['ca\.crt']}" | base64 --decode


3. The GoCD server URL for configuring the Kubernetes elastic agent plugin settings:
    echo "http://$(kubectl get service gocd-server --namespace=gocd  -o jsonpath='{.spec.clusterIP}'):8153/go"

4. The cluster URL for configuring the Kubernetes elastic agent plugin settings can be obtained by:
    kubectl cluster-info

5. Persistence
    ################################################################################################
    WARNING: The default storage class will be used. The reclaim policy for this is usually `Delete`.
    You will lose all data at the time of pod termination!
    ################################################################################################
###
kubectl get deployments --namespace gocd
kubectl get pods -n gocd --watch
kubectl get svc -n gocd 
kubectl port-forward svc/gocd-server  8080:8153 -n gocd
kubectl delete namespace gocd
```