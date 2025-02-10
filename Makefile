CHART_DIR=./controller-mq

# Kubernetes Namespace for KEDA
KEDA_NAMESPACE=keda

# Helm Release Name for KEDA
KEDA_RELEASE=consumer-autoscaler

# Helm Chart Repo for KEDA
KEDA_REPO=https://kedacore.github.io/charts

# YAML file which includes scaled objects
SCALED_OBJECT=$(CHART_DIR)/charts/keda


# Deployment files for broker, producer and consumer
BROKER_CHART=$(CHART_DIR)/charts/broker
PRODUCER_CHART=$(CHART_DIR)/charts/producer
CONSUMER_CHART=$(CHART_DIR)/charts/consumer


# Helm Install rabbitmq-broker:
install-broker:
	helm install broker $(BROKER_CHART)

# Helm Install producer:
install-producer:
	helm install producer $(PRODUCER_CHART)

# Helm install consumer:
install-consumer:
	helm install consumer $(CONSUMER_CHART)

# Helm Destroy rabbitmq-broker:
uninstall-broker:
	helm uninstall --ignore-not-found broker

# Helm Destroy producer:
uninstall-producer:
	helm uninstall --ignore-not-found producer

# Helm Destroy consumer:
uninstall-consumer:
	helm uninstall --ignore-not-found consumer

# Apply the scaling threshold changes
upgrade-scaling:
	helm upgrade --install consumer $(CONSUMER_CHART)


# Install KEDA Repo
install-keda:
	helm repo add kedacore $(KEDA_REPO)
	helm repo update
	helm install $(KEDA_RELEASE) kedacore/keda --set installCRDs=true

# Uninstall keda scaling
destroy-scaling:
	helm uninstall --ignore-not-found $(KEDA_RELEASE)
	helm repo remove kedacore