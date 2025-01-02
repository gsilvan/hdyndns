# hdyndns

An universal dynamic DNS updater for Hetzner DNS and Fritz!Box.

## Install & run your own server
### Server

```shell
# 1. Clone this repository
git clone https://github.com/gsilvan/hdyndns.git

# 2. Create the Docker image
cd hdyndns
docker build -t hdyndns .

# 3. Run the Docker image
docker run -p 127.0.0.1:56846:56846 -d hdyndns

# 4. Put nginx reverse proxy up front
vim /etc/nginx/nginx.conf

server {
    listen 80;
    listen [::]:80;
    server_name dynupdate.example.com;
    location / {
        proxy_pass http://127.0.0.1:56846;
    }
}

systemctl reload nginx

# 5. Get a SSL cert via Let's Encrypt
certbox --nginx
```

### Client

1. Log into https://dns.hetzner.com/ and get a API token.
2. Log into your Fritz!Box http://fritz.box -> Internet -> Freigaben -> DynDNS
3. Update-URL: `https://dynupdate.example.com/update?zone=<domain>&host=<username>&password=<pass>&ip=<ipaddr>`
4. Domainname: `example.com`
5. Benutzername: `dyn` (your dynamic host)
6. Kennwort: `HETZNER_API_TOKEN`
