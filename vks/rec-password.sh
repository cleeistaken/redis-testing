kubectl get secret rec -o jsonpath="{.data.password}" | base64 -d
echo
