# Controller-k8

We have created simple kubernete cluster using minikube and helm. Once deployed completely as per the steps shared in this file Kubernete cluster of Rabiitmq Broker, Producer and Consumer will be up and running.

Also, we have create custom autoscaler KDE( Kubernetes Event-Driven Autoscaling). We have deployed it within consumer subcharts to scale consumer pods by monitoring rabbitmq queue depth(ready state queue) from Rabbitmq Broker.

### Software and System Requirements

You will need the following pieces of software installed to run Controller-k8 tool.

**kubectl** - use the installation instruction on <https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/> to install kubectl

**minikube** - use the installation instruction on <https://minikube.sigs.k8s.io/docs/start/> to install minikube

**helm** - follow the instruction on <https://helm.sh/docs/intro/install/> 



## Step to setup Minkube:
I have used `docker` as a driver.
```shell
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
 
minikube start --driver=docker
```
## Step to authenticate ghcr.io:
To store custom images that we are going to pull while deploying consumer and porducer using helm charts.
```shell

tejas@ubuntu:~/minikube/Controller-k8$ docker login ghcr.io -u <your-github-username> -p <your-personal-access-token>

tejas@ubuntu:~/minikube/Controller-k8$ docker login ghcr.io
Authenticating with existing credentials...
WARNING! Your password will be stored unencrypted in /home/tejas/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

## Docker images for deploying producer and consumer.
Stored at `ghcr.io` reposatory and runtime pulled via helm charts deployment.

```shell
Build and Push images to ghcr.io

tejas@ubuntu:~/minikube/Controller-k8$ docker build -t ghcr.io/tejas-anjarlekar/one2n/my_producer:v1 -f Dockerfile.producer .

tejas@ubuntu:~/minikube/Controller-k8$ docker push ghcr.io/tejas-anjarlekar/one2n/my_producer:v1

```

```shell
docker pull ghcr.io/tejas-anjarlekar/one2n/my_producer:v1
docker pull ghcr.io/tejas-anjarlekar/one2n/my_consumer:v1
```

## Created K8 secrets:
We have manually created k8 secrets for storing Rabbitmq credentials.
```shell
kubectl create secret generic rabbitmq-secret \
  --from-literal=RABBITMQ_USERNAME=<rabbitmq user> \
  --from-literal=RABBITMQ_PASSWORD=<rabbitmq password>
```

Also, need to create k8 secrets to authenticat with `ghcr.io` when we are going to pull the images.
```shell
kubectl create secret docker-registry ghcr-auth-secret \
  --docker-server=ghcr.io \
  --docker-username=<Git Username> \
  --docker-password=<Auth Token>
```


## Clone the code:
```shell
git clone https://github.com/Tejas-Anjarlekar/Controller-k8.git

cd Controller-k8
```

## Steps to install, deploy and destroy the controller tool:
We have created Makefile for running helm command more handy.
```shell
# To deploy rabbitmq-broker pod
make install-broker
======================================
helm install broker ./controller-mq/charts/broker
NAME: broker
LAST DEPLOYED: Mon Feb 10 09:49:11 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
======================================

# To deploy producer pod
make install-producer
helm install producer ./controller-mq/charts/producer
======================================
NAME: producer
LAST DEPLOYED: Mon Feb 10 09:50:09 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
======================================

# To deploy consumer pod and keda scaler together
make install-keda
make install-consumer
======================================
helm install consumer ./controller-mq/charts/consumer
NAME: consumer
LAST DEPLOYED: Mon Feb 10 09:50:47 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
======================================

# To destroy producer pod
make uninstall-producer
======================================
tejas@ubuntu:~/minikube/Controller-k8$ make uninstall-producer
helm uninstall --ignore-not-found producer
release "producer" uninstalled
======================================

# To destroy consumer pod and keda scaler together
make uninstall-consumer
======================================
tejas@ubuntu:~/minikube/Controller-k8$ make uninstall-consumer
helm uninstall --ignore-not-found consumer
release "consumer" uninstalled
======================================

# To destroy rabbitmq-broker pod
make uninstall-broker
======================================
tejas@ubuntu:~/minikube/Controller-k8$ make uninstall-broker
helm uninstall --ignore-not-found broker
release "broker" uninstalled
======================================

# To remove keda repo
make destroy-scaling
======================================
tejas@ubuntu:~/minikube/Controller-k8$ make destroy-scaling
helm uninstall --ignore-not-found consumer-autoscaler
release "consumer-autoscaler" uninstalled
helm repo remove kedacore
"kedacore" has been removed from your repositories
======================================

# Apply the changes to consumer deployment
upgrade-scaling:
	helm upgrade --install consumer $(CONSUMER_CHART)
```

## Sample output of a cluster after complete deployment:

```shell
tejas@ubuntu:~/minikube/Controller-k8$ kubectl get pods -A
NAMESPACE     NAME                                              READY   STATUS    RESTARTS   AGE
default       consumer-6d7556666f-kmczp                         1/1     Running   0          38s
default       keda-admission-webhooks-7967d7c8dd-5lw4f          1/1     Running   0          4h44m
default       keda-operator-89c76469-qhwlb                      1/1     Running   0          4h44m
default       keda-operator-metrics-apiserver-ff6486dd4-fgp5q   1/1     Running   0          4h44m
default       producer-65b7985f45-zs9j2                         1/1     Running   0          76s
default       rabbitmq-broker-666784dd9f-d8vr9                  1/1     Running   0          2m14s
kube-system   coredns-668d6bf9bc-wxrtj                          1/1     Running   0          8h
kube-system   etcd-minikube                                     1/1     Running   0          8h
kube-system   kube-apiserver-minikube                           1/1     Running   0          8h
kube-system   kube-controller-manager-minikube                  1/1     Running   0          8h
kube-system   kube-proxy-j7bxz                                  1/1     Running   0          8h
kube-system   kube-scheduler-minikube                           1/1     Running   0          8h
kube-system   storage-provisioner                               1/1     Running   0          8h
```

## Sample output of cluster after destroy:
```shell
Only Minikube node is running:
======================================
tejas@ubuntu:~/minikube/Controller-k8$ kubectl  get pods -A
NAMESPACE     NAME                               READY   STATUS    RESTARTS   AGE
kube-system   coredns-668d6bf9bc-wxrtj           1/1     Running   0          9h
kube-system   etcd-minikube                      1/1     Running   0          9h
kube-system   kube-apiserver-minikube            1/1     Running   0          9h
kube-system   kube-controller-manager-minikube   1/1     Running   0          9h
kube-system   kube-proxy-j7bxz                   1/1     Running   0          9h
kube-system   kube-scheduler-minikube            1/1     Running   0          9h
kube-system   storage-provisioner                1/1     Running   0          9h
```

## How to access Rabbitmq Broker Management UI:
We have used official docker images `rabbitmq:3-management` to deploy a rabbitmq broker pod.
Also, created service `NodePort` to access broker from external network and by default pods will connect with each other using `ClusterIP` service.

To access Rabbitmq broker UI on your local:

```shell
To get custom port mapped with your local machine(30000):


tejas@ubuntu:~/minikube/Controller-k8$ kubectl get svc
NAME                              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                          AGE
keda-admission-webhooks           ClusterIP   10.106.112.137   <none>        443/TCP                          4h48m
keda-operator                     ClusterIP   10.97.140.215    <none>        9666/TCP                         4h48m
keda-operator-metrics-apiserver   ClusterIP   10.98.90.29      <none>        443/TCP,8080/TCP                 4h48m
kubernetes                        ClusterIP   10.96.0.1        <none>        443/TCP                          8h
rabbitmq-broker                   NodePort    10.107.44.215    <none>        5672:32100/TCP,15672:30000/TCP   6m15s

To get IP of Minikube node to access UI from browser

tejas@ubuntu:~/minikube/Controller-k8$ minikube ip
192.168.49.2

http://192.168.49.2:30000/#/
```
## Check scaling of consumer pods:
Once cluster is UP, KEDA will trigger scaling of consumer noder as rabbitmq queue deapth(ready state queue) is increases:

```shell
tejas@ubuntu:~/minikube/Controller-k8$ kubectl get hpa -w
NAME                                REFERENCE             TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
keda-hpa-rabbitmq-consumer-scaler   Deployment/consumer   12/20 (avg)   1         3         1          11m
keda-hpa-rabbitmq-consumer-scaler   Deployment/consumer   15/20 (avg)   1         3         1          11m
keda-hpa-rabbitmq-consumer-scaler   Deployment/consumer   18/20 (avg)   1         3         1          11m
keda-hpa-rabbitmq-consumer-scaler   Deployment/consumer   21/20 (avg)   1         3         1          12m
keda-hpa-rabbitmq-consumer-scaler   Deployment/consumer   24/20 (avg)   1         3         1          12m
keda-hpa-rabbitmq-consumer-scaler   Deployment/consumer   0/20 (avg)    1         3         2          12m
```

## Some useful commands for verifiation and troubleshooting:
```shell
tejas@ubuntu:~/minikube/Controller-k8$ kubectl describe hpa keda-hpa-rabbitmq-consumer-scaler
Name:                                               keda-hpa-rabbitmq-consumer-scaler
Namespace:                                          default
Labels:                                             app.kubernetes.io/managed-by=Helm
                                                    app.kubernetes.io/name=keda-hpa-rabbitmq-consumer-scaler
                                                    app.kubernetes.io/part-of=rabbitmq-consumer-scaler
                                                    app.kubernetes.io/version=2.16.1
                                                    scaledobject.keda.sh/name=rabbitmq-consumer-scaler
Annotations:                                        meta.helm.sh/release-name: consumer
                                                    meta.helm.sh/release-namespace: default
CreationTimestamp:                                  Mon, 10 Feb 2025 09:50:47 -0800
Reference:                                          Deployment/consumer
Metrics:                                            ( current / target )
  "s0-rabbitmq-test_queue" (target average value):  0 / 20
Min replicas:                                       1
Max replicas:                                       3
Deployment pods:                                    2 current / 2 desired
Conditions:
  Type            Status  Reason               Message
  ----            ------  ------               -------
  AbleToScale     True    ScaleDownStabilized  recent recommendations were higher than current one, applying the highest recent recommendation
  ScalingActive   True    ValidMetricFound     the HPA was able to successfully calculate a replica count from external metric s0-rabbitmq-test_queue(&LabelSelector{MatchLabels:map[string]string{scaledobject.keda.sh/name: rabbitmq-consumer-scaler,},MatchExpressions:[]LabelSelectorRequirement{},})
  ScalingLimited  False   DesiredWithinRange   the desired count is within the acceptable range
Events:
  Type    Reason             Age                    From                       Message
  ----    ------             ----                   ----                       -------
  Normal  SuccessfulRescale  4m54s                  horizontal-pod-autoscaler  New size: 1; reason: All metrics below target
  Normal  SuccessfulRescale  2m24s (x2 over 9m55s)  horizontal-pod-autoscaler  New size: 2; reason: external metric s0-rabbitmq-test_queue(&LabelSelector{MatchLabels:map[string]string{scaledobject.keda.sh/name: rabbitmq-consumer-scaler,},MatchExpressions:[]LabelSelectorRequirement{},}) above target


$ yamllint controller-mq/templates/rabbitmq-broker.yaml
$ helm template . | kubectl apply --dry-run=client -f -
$ helm lint
$ kubectl run -it --rm --image=busybox dns-test --restart=Never -- nslookup rabbitmq-broker-default.svc.cluster.local
```