# NIFI

# helm chart

```bash
# repo
helm repo add cetic https://cetic.github.io/helm-charts
helm repo update
# search version

# pull charts



```


# docker run 
[docker hub](https://hub.docker.com/r/apache/nifi)
```bash 
# docker run 
docker run --name nifi -p 9992:9992 \
-e NIFI_WEB_HTTPS_PORT='9992' \
-e SINGLE_USER_CREDENTIALS_USERNAME=aicel \
-e SINGLE_USER_CREDENTIALS_PASSWORD=Aicel2022! \
-d apache/nifi:1.19.1

# credential from logs
docker logs -f nifi

Generated Username [05d65c47-85ec-401c-8e0f-a6c7f72350e4]
Generated Password [y5zY6WSETfCqKVR/8nw1ip8QRbU8oyQm]

```