# urlencoder
Encode and decode a string of text
## Setup
### production
```
docker-compose -f docker-compose.prod.yml up -d
```
Go to `http://host-ip:8000`, type or paste your input data and press the encode/decode button.  
If you want to change the port number, change the environment variable `GUNICORN_PORT` in Dockerfile.
### development
```
docker-compose -f docker-compose.dev.yml up -d
```
Go to `http://localhost:5000`, you can access the development environment.
If you want to change the port number, change the environment variable `FLASK_RUN_PORT` in Dockerfile.
### initial
```
docker-compose -f docker-compose.init.yml up -d
```
This is a dedicated environment for executing `poetry init`.
