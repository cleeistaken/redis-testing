# Setup Redis on VKS Cluster

```shell
# Create namespace
kubectl create ns redis

# Change to redis context
kubectl config set-context --current --namespace redis

# Redis OSS Operator install
helm install my-release oci://registry-1.docker.io/bitnamicharts/redis-cluster -f values.yaml --set "cluster.nodes=12,persistence.size=400Gi,usePassword=false,cluster.replicas=2,redis.resourcesPreset=none"

# To log into the Redis cluster management UI, go to https://<lb-ip>:8443 (username: demo@redis.com, password retrieved in step 6)
kubectl apply -f redis-client-pod.yaml

# check if client pod runs on a separate host
kubectl exec -it ubuntu -- bash
```