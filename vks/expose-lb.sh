rec=rec-ui
kubectl expose service ${rec} --type=LoadBalancer --name=${rec}-external
sleep 10
kubectl get svc


