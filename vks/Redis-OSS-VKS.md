# Setup Redis on VKS Cluster

```shell
# Create namespace
kubectl create ns redis

# Change to redis context
kubectl config set-context --current --namespace redis

# Redis Enterprise Operator install
kubectl apply -f bundle.yaml

# Redis Enterprise Install
kubectl apply -f rec.yaml
kubectl get rec --watch
kubectl apply -f redb1.yaml
kubectl get redb --watch

#
expose-lb.sh
rec-password.sh
redb1-password.sh

# To log into the Redis cluster management UI, go to https://<lb-ip>:8443 (username: demo@redis.com, password retrieved in step 6)
kubectl apply -f redis-client-pod.yaml

# check if client pod runs on a separate host
kubectl exec -it ubuntu -- bash
```