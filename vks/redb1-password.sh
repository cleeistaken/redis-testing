kubectl get secret redb-redb1 -o jsonpath="{.data.password}" | base64 -d
echo
