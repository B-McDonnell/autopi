There must exist a keys folder in the root for docker to copy the keys correctly. They must be named as follows.

```
tls/
|
|--- autopi_server.cer
|--- autopi_server.key
```

The Shibboleth service provider is integrated with Apache. For some reason, Shibboleth fails if the docker container is not removed before being started. In other words, you must invoke `docker-compose down` before executing `docker-compose up`. If you have made configuration changes to any part of the system other than the docker-compose.yaml file itself, make sure to run `docker-compose build` first or run `docker-compose up --build`. The server certificate and private key can be changed without rebuilding the containers.
