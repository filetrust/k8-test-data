###Start minikube
    minikube start --driver=virtualbox
###Create ECK operator
    kubectl apply -f https://download.elastic.co/downloads/eck/1.2.1/all-in-one.yaml
    kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
###Deploy ELK. This may take 5+ minutes.
    kubectl apply -f tenant.yml
###Check the credentials
###Username: elastic Password: see command below

    kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'
###Open Kibana on https://localhost:5601
    kubectl port-forward service/quickstart-kb-http 5601