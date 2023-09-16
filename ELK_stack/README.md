```shell

kubectl port-forward svc/elasticsearch 9200

curl http://localhost:9200/_cat/health?v
curl http://localhost:9200/_cluster/state?pretty


kubectl port-forward svc/kibana 5601 


```