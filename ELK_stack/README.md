```shell

kubectl port-forward svc/elasticsearch 9200

curl http://localhost:9200/_cat/health?v
curl http://localhost:9200/_cluster/state?pretty


kubectl port-forward svc/kibana 5601 


# Create SealedSecret for the admin elasticsearch password
kubectl  create secret generic elastic-credentials \  
  --from-literal=ELASTIC_PASSWORD='STRONG-PASSWORD' \
  --dry-run=client -o yaml | ${KUBESEAL_BINARY} --cert ${KUBESEAL_CERT_PATH} --format yaml > SealedSecret-ElasticCredentials.yaml


# Create SealedSecret for the admin elasticsearch password
kubectl  create secret generic elastic-credentials --from-literal=ELASTIC_PASSWORD='STRONG-PASSWORD' --dry-run=client -o yaml > elasticCredentials.yaml


#Elasticsearch will fail to start when the security feature is ON without security configuration is configured!
#Before we can enable the security feature, we need to generate certificates for elasticsearch nodes. Elasticsearch nodes will communicate securely with each other. 
#Run the following commands in the elasticsearch container.

kubectl  exec -ti es-cluster-0 -- bash
  
# Create certificates
elasticsearch-certutil ca --out /tmp/elastic-stack-ca.p12 --pass ''
elasticsearch-certutil cert --name security-master --dns security-master --ca /tmp/elastic-stack-ca.p12 --pass '' --ca-pass '' --out /tmp/elastic-certificates.p12
 
# copy certificates to local machine
kubectl cp es-cluster-0:/tmp/elastic-stack-ca.p12 ./elastic-stack-ca.p12
kubectl cp es-cluster-0:/tmp/elastic-certificates.p12 ./elastic-certificates.p12
 
# Validate and extract PEM
openssl pkcs12 -nodes -passin pass:'' -in elastic-certificates.p12 -out elastic-certificate.pem

#Once we have generated our certificate and copied it from the container to our local machine, we will create a SealedSecret from the PEM file. We will mount this PEM file to the container later.

# Create SealedSecret for the P12 file
kubectl -n elasticsearch create secret generic elastic-certificate-pem \
  --from-file=elastic-certificates.p12 \
  --dry-run=client -o yaml | ${KUBESEAL_BINARY} --cert ${KUBESEAL_CERT_PATH} --format yaml > SealedSecret-ElasticCertificates.yaml

# Create SealedSecret for the P12 file
kubectl create secret generic elastic-certificate-pem --from-file=elastic-certificates.p12 --dry-run=client -o yaml > elasticsearch_certificates.yaml


# if the pods are not restarted automatically, scale down statefulset and scale back up:
kubectl  scale statefulset es-cluster --replicas 0
#wait till all nodes are deleted
 
kubectl  scale statefulset es-cluster --replicas 3


# Kibana Username and Password

# When we launch Kibana, the first question Kibana asks us is: "What is the username and password of the Kibana user". The username is kibana_system. The password can be retrieved from within the Elasticsearch container. 
#Exec to one of the Elasticsearch containers and run the following command:


kubectl  exec -ti es-cluster-0 -- bash
 
#This will generate a random string. Save the password!
./bin/elasticsearch-reset-password -u kibana_system

# Creating Kibana credentials
kubectl  create secret generic kibana-credentials --from-literal=ELASTICSEARCH_PASSWORD='STRONG-PASSWORD' --dry-run=client -o yaml > kibana_credentials.yaml


# Create secret for the P12 file
kubectl create secret generic kibana-certificate-pem --from-file=elastic-certificates.p12 --dry-run=client -o yaml > kibana_certificates.yaml
```