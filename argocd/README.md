```shell
kubectl create namespace argocd
kubectl apply -n argocd -f install.yaml
kubectl get pods -n argocd --watch
brew install argocd
argocd admin initial-password -n argocd
qWUd94dqBj7ylSKi
 This password must be only used for first time login. We strongly recommend you update the password using `argocd account update-password`
kubectl port-forward svc/argocd-server -n argocd 8080:443
argocd login <ARGOCD_SERVER>
argocd account update-password
kubectl config get-contexts -o name
argocd cluster add docker-desktop
argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default
```
# url 
[docs] (https://argo-cd.readthedocs.io/en/stable/getting_started/)
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Creating Apps Via CLI
```shell
kubectl config set-context --current --namespace=argocd
argocd app create guestbook --repo https://github.com/argoproj/argocd-example-apps.git --path guestbook --dest-server https://kubernetes.default.svc --dest-namespace default
argocd app get guestbook
argocd app sync guestbook
kubectl port-forward svc/guestbook-ui  8081:80
kubectl delete namespace argocd
kubectl delete deployment guestbook-ui
kubectl delete svc guestbook-ui
```