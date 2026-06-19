## Description

Le fichier docker-compose.yml définit trois conteneurs Docker : un HAProxy acceptant les connexions sur le port 5000 de l'hôte, et deux conteneurs nginx non exposés à l'hôte.

La personne ayant configuré ce système souhaitait placer HAProxy devant les conteneurs nginx (backend ou upstream) pour répartir la charge, mais cela ne fonctionne pas.

---

## Test

```bash
curl localhost:5000
```

## Resultat

```bash
hello there from nginx_0
```

## Test

```bash
docker compose logs
```

## Resultat

```bash
haproxy  | [NOTICE]   (1) : config : [/usr/local/etc/haproxy/haproxy.cfg:19] : 'server nginx_backends/nginx_1' : could not resolve address 'nginx_1', disabling server.
haproxy  | [NOTICE]   (1) : New worker (8) forked
haproxy  | [NOTICE]   (1) : Loading success.
nginx_0  | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx_0  | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx_0  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx_0  | 10-listen-on-ipv6-by-default.sh: info: can not modify /etc/nginx/conf.d/default.conf (read-only file system?)
nginx_0  | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx_0  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx_0  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx_0  | /docker-entrypoint.sh: Configuration complete; ready for start up
nginx_0  | 2026/06/19 20:10:06 [notice] 1#1: using the "epoll" event method
nginx_0  | 2026/06/19 20:10:06 [notice] 1#1: nginx/1.25.3
nginx_0  | 2026/06/19 20:10:06 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
nginx_0  | 2026/06/19 20:10:06 [notice] 1#1: OS: Linux 5.10.0-23-cloud-amd64
nginx_0  | 2026/06/19 20:10:06 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
nginx_0  | 2026/06/19 20:10:06 [notice] 1#1: start worker processes
nginx_0  | 2026/06/19 20:10:06 [notice] 1#1: start worker process 20
nginx_0  | 2026/06/19 20:10:06 [notice] 1#1: start worker process 21
nginx_0  | 172.18.0.2 - - [19/Jun/2026:20:10:14 +0000] "GET / HTTP/1.1" 200 25 "-" "curl/7.74.0" "-"
nginx_0  | 172.18.0.2 - - [19/Jun/2026:20:10:16 +0000] "GET / HTTP/1.1" 200 25 "-" "curl/7.74.0" "-"
nginx_0  | 172.18.0.2 - - [19/Jun/2026:20:10:17 +0000] "GET / HTTP/1.1" 200 25 "-" "curl/7.74.0" "-"
nginx_0  | 172.18.0.2 - - [19/Jun/2026:20:10:21 +0000] "GET / HTTP/1.1" 200 25 "-" "curl/7.74.0" "-"
nginx_0  | 172.18.0.2 - - [19/Jun/2026:20:10:21 +0000] "GET / HTTP/1.1" 200 25 "-" "curl/7.74.0" "-"
nginx_0  | 172.18.0.2 - - [19/Jun/2026:20:10:21 +0000] "GET / HTTP/1.1" 200 25 "-" "curl/7.74.0" "-"
nginx_0  | 172.18.0.2 - - [19/Jun/2026:20:10:21 +0000] "GET / HTTP/1.1" 200 25 "-" "curl/7.74.0" "-"
nginx_0  | 172.18.0.2 - - [19/Jun/2026:20:10:21 +0000] "GET / HTTP/1.1" 200 25 "-" "curl/7.74.0" "-"
nginx_0  | 172.18.0.2 - - [19/Jun/2026:20:13:43 +0000] "GET / HTTP/1.1" 200 25 "-" "curl/7.74.0" "-"
nginx_1  | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
nginx_1  | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
nginx_1  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
nginx_1  | 10-listen-on-ipv6-by-default.sh: info: can not modify /etc/nginx/conf.d/default.conf (read-only file system?)
nginx_1  | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
nginx_1  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
nginx_1  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
nginx_1  | /docker-entrypoint.sh: Configuration complete; ready for start up
nginx_1  | 2026/06/19 20:10:06 [notice] 1#1: using the "epoll" event method
nginx_1  | 2026/06/19 20:10:06 [notice] 1#1: nginx/1.25.3
nginx_1  | 2026/06/19 20:10:06 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
nginx_1  | 2026/06/19 20:10:06 [notice] 1#1: OS: Linux 5.10.0-23-cloud-amd64
nginx_1  | 2026/06/19 20:10:06 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
nginx_1  | 2026/06/19 20:10:06 [notice] 1#1: start worker processes
nginx_1  | 2026/06/19 20:10:06 [notice] 1#1: start worker process 21
nginx_1  | 2026/06/19 20:10:06 [notice] 1#1: start worker process 22
```

## Solution

```bash
cat cat custom-nginx_1.conf 
```

### To change

```
server {
    listen 80;

    server_name localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html;
    }
}
```

### For

```
server {
    listen 81;

    server_name localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html;
    }
}
```


### To change

```bash
  haproxy:
    image: haproxy:2.8.4
    container_name: haproxy
    restart: always
    ports:
      - "5000:5000"
    depends_on:
      - nginx_0
      - nginx_1
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
    networks:
      - frontend_network
```

### For
```bash
  haproxy:
    image: haproxy:2.8.4
    container_name: haproxy
    restart: always
    ports:
      - "5000:5000"
    depends_on:
      - nginx_0
      - nginx_1
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
    networks:
      - frontend_network
      - backend_network
```

## Explanation

> Le fichier **custom-nginx_0.conf** et **custom-nginx_1.conf** contienne le même port, donc on avait un conflit et dans le fichier docker-compose.yml, le service haproxy n'avais pas le réseau pour communiquer avec **nginx_1** qui est sous le réseau **backend_network**