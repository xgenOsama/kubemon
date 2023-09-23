# install using helm

```shell
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install kafka bitnami/kafka
kubectl get pods -n kafka
kubectl scale deployment kafka --replicas=<number of replicas>
kubectl scale deployment kafka --replicas=3

```

# normal install 

```shell
kubectl port-forward svc/kafka-service  9092 -n kafka

echo "hello world!" | kafkacat -P -b localhost:9092 -t test
# The command should execute without errors, indicating that producers are communicating fine with Kafka in k8s. How do we see what messages are currently on the queue named test? We run the following command:
kafkacat -C -b localhost:9092 -t test

```