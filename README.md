# tgc2rss

## Installation

- Install the dependendencies via Poetry:
```sh
poetry install --with dev
```

- Install the pre-commit hooks:
```sh
pre-commit install
```

- Run the application:
```sh
python src/app.py
```



## Run via Docker

- Build an image:
```sh
docker build -t tgc2rss .
```
- Run a container from your image:
```sh
docker run -d -p 3000:3000 tgc2rss
```

## Run via Docker Compose

You can start whole cluster containing Kafka using next command:
```sh
docker compose up --build
```
