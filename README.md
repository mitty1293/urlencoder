# urlencoder
Encode and decode a string of text

Access https://urlencoder.fmitty.net/, type or paste your input data and press the encode/decode button.
## Self hosting
### Production Environment(via traefik)
Replace the value of DOMAIN with the domain.
```
# Copy .env_example as .env
cp .env_example .env
vi .env
```
```
# Replace the value of DOMAIN in .env
DOMAIN=example.com
```
Start the container.
```
docker network create traefik_reverse_proxy_network
docker compose -f docker-compose.traefik.yml up -d
```
Go to `https://urlencoder.${DOMAIN}`, type or paste your input data and press the encode/decode button.  
### production(Standalone)
```
docker compose -f docker-compose.prod.yml up -d
```
Go to `https://host-ip:8000`, type or paste your input data and press the encode/decode button.  
If you want to change the port number, change the environment variable `GUNICORN_PORT` in Dockerfile and `ports` in docker-compose file.
### development
```
docker compose -f docker-compose.dev.yml up -d
```
Go to `https://host-ip:5000`, you can access the development environment.
If you want to change the port number, change the environment variable `FLASK_RUN_PORT` in Dockerfile and `ports` in docker-compose file.
### initial
```
docker compose -f docker-compose.init.yml up -d
```
This is a dedicated environment for executing `poetry init`.
