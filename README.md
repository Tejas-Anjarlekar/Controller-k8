# Controller-k8

We have created simple kubernete cluster sing minikube and helm. Once deployed completely as per the steps shared in this file Kubernete cluster of Rabiitmq Broker, Producer and Consumer will be up and running.

Also, we have create custom autoscaler KDE( Kubernetes Event-Driven Autoscaling). We have deployed it within consumer subcharts to scale consumer pods by monitoring rabbitmq queue depth(ready state queue) from Rabbitmq Broker.

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
