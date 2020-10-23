# Glasswall Rebuild Service

### Usage

`docker build -t glasswall-rebuild .`

### To push

`docker push <username>/glasswall-rebuild`

### Endpoints 

| Endpoint | Description             | Payload     |
| -------- | ------------------------| ----------- |
| `/process` | Send malicious file and get cleaned file   | `{"file": "<raw file>"}` |	

