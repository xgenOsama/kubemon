# install CRD Install ECK Operator
* CustomResourceDefinition objects for all supported resource types (Elasticsearch, Kibana, APM Server, Enterprise Search, Beats, Elastic Agent, and Elastic Maps Server).
* Namespace named elastic-system to hold all operator resources.
* ServiceAccount, ClusterRole and ClusterRoleBinding to allow the operator to manage resources throughout the cluster
* ValidatingWebhookConfiguration to validate Elastic custom resources on admission
* StatefulSet, ConfigMap, Secret and Service in elastic-system namespace to run the operator application
```shell
# install custom resource definitions
# this will create custom crds for elasticsearch
kubectl create -f https://download.elastic.co/downloads/eck/2.3.0/crds.yaml

❯❯ kubectl get crd
NAME                                                 CREATED AT
agents.agent.k8s.elastic.co                          2022-07-30T02:16:25Z
apmservers.apm.k8s.elastic.co                        2022-07-30T02:16:25Z
beats.beat.k8s.elastic.co                            2022-07-30T02:16:25Z
elasticmapsservers.maps.k8s.elastic.co               2022-07-30T02:16:25Z
elasticsearches.elasticsearch.k8s.elastic.co         2022-07-30T02:16:25Z
enterprisesearches.enterprisesearch.k8s.elastic.co   2022-07-30T02:16:25Z
kibanas.kibana.k8s.elastic.co                        2022-07-30T02:16:26Z


---

# install the operator with its RBAC rules
# this will create namespace called elastic-system and install elastic operator on it
kubectl apply -f https://download.elastic.co/downloads/eck/2.3.0/operator.yaml

❯❯ kubectl get all -n elastic-system
NAME                     READY   STATUS    RESTARTS   AGE
pod/elastic-operator-0   1/1     Running   0          25h

NAME                             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
service/elastic-webhook-server   ClusterIP   10.100.135.188   <none>        443/TCP   25h

NAME                                READY   AGE
statefulset.apps/elastic-operator   1/1     25h


# deploy elasticsearch
kubectl apply -f elasticsearch.yaml

❯❯ kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
rahasak-elasticsearch-es-client-0   0/1     Running   0          49s
rahasak-elasticsearch-es-data-0     0/1     Running   0          8s
rahasak-elasticsearch-es-master-0   0/1     Running   0          8s

❯❯ kubectl get svc
NAME                                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kubernetes                               ClusterIP   10.96.0.1       <none>        443/TCP    27h
rahasak-elasticsearch-es-client          ClusterIP   None            <none>        9200/TCP   4s
rahasak-elasticsearch-es-data            ClusterIP   None            <none>        9200/TCP   5s
rahasak-elasticsearch-es-http            ClusterIP   10.110.62.112   <none>        9200/TCP   7s
rahasak-elasticsearch-es-internal-http   ClusterIP   10.108.155.65   <none>        9200/TCP   7s
rahasak-elasticsearch-es-master          ClusterIP   None            <none>        9200/TCP   5s
rahasak-elasticsearch-es-transport       ClusterIP   None            <none>        9300/TCP   7s

❯❯ kubectl get pvc
NAME                                                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
elasticsearch-data-rahasak-elasticsearch-es-client-0   Bound    pvc-f9a3eb19-cd97-443e-8d45-676c056569d2   1Gi        RWO            standard       40s
elasticsearch-data-rahasak-elasticsearch-es-data-0     Bound    pvc-ef6c7d7b-6109-42a2-b11d-24c3dfa0cd1e   1Gi        RWO            standard       41s
elasticsearch-data-rahasak-elasticsearch-es-master-0   Bound    pvc-a73e810a-75d2-4c19-9785-f89da4087f1c   1Gi        RWO            standard       41s

❯❯ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                                          STORAGECLASS   REASON   AGE
pvc-a73e810a-75d2-4c19-9785-f89da4087f1c   1Gi        RWO            Delete           Bound    default/elasticsearch-data-rahasak-elasticsearch-es-master-0   standard                52s
pvc-ef6c7d7b-6109-42a2-b11d-24c3dfa0cd1e   1Gi        RWO            Delete           Bound    default/elasticsearch-data-rahasak-elasticsearch-es-data-0     standard                51s
pvc-f9a3eb19-cd97-443e-8d45-676c056569d2   1Gi        RWO            Delete           Bound    default/elasticsearch-data-rahasak-elasticsearch-es-client-0   standard                51s



# secret object for elastic user
❯❯ kubectl get secret rahasak-elasticsearch-es-elastic-user
NAME                                    TYPE     DATA   AGE
rahasak-elasticsearch-es-elastic-user   Opaque   1      3m26s

# get password
❯❯ PASSWORD=$(kubectl get secret rahasak-elasticsearch-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode)

❯❯ echo $PASSWORD
67J929LvWs5nl8XbN1g2JK2U



# port forward cluster ip service
❯❯ kubectl port-forward service/rahasak-elasticsearch-es-http 9200
Forwarding from 127.0.0.1:9200 -> 9200
Forwarding from [::1]:9200 -> 9200

# elastic password
PASSWORD=$(kubectl get secret rahasak-elasticsearch-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode)

# access elasticsearch api via curl with baseic auth
❯❯ curl -u "elastic:$PASSWORD" -k "https://localhost:9200"
{
  "name" : "rahasak-elasticsearch-es-client-0",
  "cluster_name" : "rahasak-elasticsearch",
  "cluster_uuid" : "Z8EPZsYXQGu1GcRBUXAQMA",
  "version" : {
    "number" : "7.6.2",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "ef48eb35cf30adf4db14086e8aabd07ef6fb113f",
    "build_date" : "2020-03-26T06:34:37.794943Z",
    "build_snapshot" : false,
    "lucene_version" : "8.4.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}




# deploy kibana
❯❯ kubectl apply -f kibana.yaml

# available pods
❯❯ kubectl get pods
NAME                                        READY   STATUS    RESTARTS   AGE
rahasak-elasticsearch-es-client-0           1/1     Running   0          11m
rahasak-elasticsearch-es-data-0             0/1     Pending   0          11m
rahasak-elasticsearch-es-master-0           1/1     Running   0          11m
rahasak-elasticsearch-kb-84d645655d-5r8bs   0/1     Running   0          75s

# available services
❯❯ kubectl get svc
NAME                                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kubernetes                               ClusterIP   10.96.0.1        <none>        443/TCP    27h
rahasak-elasticsearch-es-client          ClusterIP   None             <none>        9200/TCP   12m
rahasak-elasticsearch-es-data            ClusterIP   None             <none>        9200/TCP   12m
rahasak-elasticsearch-es-http            ClusterIP   10.110.62.112    <none>        9200/TCP   12m
rahasak-elasticsearch-es-internal-http   ClusterIP   10.108.155.65    <none>        9200/TCP   12m
rahasak-elasticsearch-es-master          ClusterIP   None             <none>        9200/TCP   12m
rahasak-elasticsearch-es-transport       ClusterIP   None             <none>        9300/TCP   12m
rahasak-elasticsearch-kb-http            ClusterIP   10.104.204.112   <none>        5601/TCP   86s



# port forward kibana cluster ip service
❯❯ kubectl port-forward service/rahasak-elasticsearch-kb-http 5601
Forwarding from 127.0.0.1:5601 -> 5601
Forwarding from [::1]:5601 -> 5601

# get password for elastic user
PASSWORD=$(kubectl get secret rahasak-elasticsearch-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode)

❯❯ echo $PASSWORD
67J929LvWs5nl8XbN1g2JK2U

```