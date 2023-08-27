kubectl create namespace jenkins
kubectl get services --namespace jenkins
kubectl get pods --namespace jenkins
kubectl logs jenkins-6fb994cfc5-twnvn -n jenkins
kubectl  -n jenkins exec  jenkins-56b6774bb6-47bk8 -- cat  /var/jenkins_home/secrets/initialAdminPassword 
kubectl  -n jenkins exec  jenkins-56b6774bb6-47bk8 -- cat  /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
kubectl port-forward svc/jenkins-service  8080:8080 -n jenkins